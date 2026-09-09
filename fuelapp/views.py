import base64
import io
import pandas as pd
import numpy as np
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, accuracy_score
import joblib
import os
from .models import ECUData, UserProfile, PredictionResult

# ─────────────────────────────────────────────────────────────────────
# Admin credentials
# ─────────────────────────────────────────────────────────────────────
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# NOTE: raw_fuel_to_lph() and its LOG constants have been removed.
# The dataset already stores real LPH values (1.5 – 15.0), so no
# logarithmic re-scaling from a "raw" domain is needed.


# ─────────────────────────────────────────────────────────────────────
# Driving profile scorer
# Returns a dict of {profile: score_0_to_100} calculated from the
# actual driving parameters.  The highest-scoring profile IS the
# declared driving style — used in both predict_fuel() and Chart 3.
# ─────────────────────────────────────────────────────────────────────
def calc_profile_scores(speed, rpm, throttle, load, acceleration, gear_position):
    """
    Score each driving profile 0–100 based on the input parameters.
    Scores are independent (not forced to sum to 100) so each profile
    reflects purely how closely the inputs match that style.
    The profile with the highest score is the detected driving style.
    """
    scores = {}

    # ── Aggressive ────────────────────────────────────────────────────
    # High throttle, high RPM, hard acceleration, low gear
    scores['Aggressive'] = min(100, round(
        (throttle / 100) * 35 +
        (min(rpm, 7000) / 7000) * 25 +
        (min(max(acceleration, 0), 5) / 5) * 25 +
        (max(0, 4 - gear_position) / 3) * 15
    , 1))

    # ── Eco-Friendly ──────────────────────────────────────────────────
    # Low throttle, low RPM, gentle acceleration, higher gear
    scores['Eco-Friendly'] = min(100, round(
        (max(0, 100 - throttle) / 100) * 35 +
        (max(0, 3000 - rpm) / 3000) * 25 +
        (max(0, 2.0 - abs(acceleration)) / 2.0) * 25 +
        (min(gear_position, 6) / 6) * 15
    , 1))

    # ── City ──────────────────────────────────────────────────────────
    # Low-to-medium speed, frequent speed changes, low gear
    scores['City'] = min(100, round(
        (max(0, 70 - speed) / 70) * 40 +
        (min(abs(acceleration), 3) / 3) * 30 +
        (max(0, 4 - gear_position) / 3) * 30
    , 1))

    # ── Highway ───────────────────────────────────────────────────────
    # High speed, high gear, steady throttle, smooth acceleration
    scores['Highway'] = min(100, round(
        (min(max(speed - 60, 0), 120) / 120) * 40 +
        (min(gear_position, 6) / 6) * 30 +
        (max(0, 80 - throttle) / 80) * 20 +
        (max(0, 1.5 - abs(acceleration)) / 1.5) * 10
    , 1))

    # ── Moderate ──────────────────────────────────────────────────────
    # Middle-of-the-road on all metrics — score based on how
    # "average" the inputs are (distance from extremes)
    throttle_mid = max(0, 50 - abs(throttle - 45)) / 50
    rpm_mid      = max(0, 50 - abs((rpm - 2500) / 45)) / 50
    speed_mid    = max(0, 50 - abs(speed - 65)) / 50
    accel_mid    = max(0, 1.0 - abs(acceleration)) / 1.0
    scores['Moderate'] = min(100, round(
        throttle_mid * 30 +
        rpm_mid      * 25 +
        speed_mid    * 25 +
        accel_mid    * 20
    , 1))

    return scores


# ─────────────────────────────────────────────────────────────────────
# ML model
# ─────────────────────────────────────────────────────────────────────
ml_model = None
scaler = None
model_trained = False


class AdvancedFuelConsumptionPredictor:
    def __init__(self):
        self.regressor  = RandomForestRegressor(n_estimators=200, random_state=42)
        self.classifier = RandomForestClassifier(n_estimators=200, random_state=42)
        self.scaler     = StandardScaler()
        self.is_trained = False

    def train(self, X, y_reg, y_clf):
        # y_reg already contains real LPH values (1.5 – 15.0).
        # log1p is applied only for training stability (compresses variance);
        # expm1 in predict() reverses it exactly — no further conversion needed.
        y_reg_log = np.log1p(y_reg)
        X_scaled  = self.scaler.fit_transform(X)
        self.regressor.fit(X_scaled, y_reg_log)
        self.classifier.fit(X_scaled, y_clf)
        self.is_trained = True

    def predict(self, X):
        if not self.is_trained:
            raise Exception("Model not trained")
        X_scaled      = self.scaler.transform(X)
        log_fuel_pred = self.regressor.predict(X_scaled)[0]

        # ✅ FIX: expm1 reverses log1p → result is already real LPH.
        # raw_fuel_to_lph() has been removed; it was compressing real LPH
        # values through a log scale calibrated for a completely different
        # dataset (raw values up to ~364,000), crushing e.g. 15 LPH → 4 LPH.
        lph = float(np.expm1(log_fuel_pred))
        lph = round(float(np.clip(lph, 1.5, 15.0)), 2)

        profile_pred = self.classifier.predict(X_scaled)[0]
        return lph, profile_pred


# ─────────────────────────────────────────────────────────────────────
# Standard views
# ─────────────────────────────────────────────────────────────────────
def home(request):
    return render(request, 'home.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            request.session['admin_logged_in'] = True
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid admin credentials')
    return render(request, 'admin_login.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'user_login.html')


def register(request):
    if request.method == 'POST':
        username      = request.POST['username']
        email         = request.POST['email']
        password      = request.POST['password']
        phone         = request.POST['phone']
        vehicle_model = request.POST['vehicle_model']
        license_plate = request.POST['license_plate']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            UserProfile.objects.create(
                user=user,
                phone_number=phone,
                vehicle_model=vehicle_model,
                license_plate=license_plate
            )
            messages.success(request, 'Registration successful! Please login.')
            return redirect('user_login')
    return render(request, 'register.html')


@login_required
def user_dashboard(request):
    return render(request, 'user_dashboard.html')


def admin_dashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    return render(request, 'admin_dashboard.html')


def upload_dataset(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    if request.method == 'POST' and request.FILES.get('dataset'):
        dataset_file = request.FILES['dataset']
        try:
            df = pd.read_csv(dataset_file)
            messages.success(request, 'Dataset uploaded successfully!')
            return redirect('train_model')
        except Exception as e:
            messages.error(request, f'Error processing dataset: {str(e)}')
    return render(request, 'upload_dataset.html')


def train_model(request):
    global ml_model, model_trained

    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    try:
        df = pd.read_csv('dataset/ecu_fuel_consumption_data.csv')

        features = ['vehicle_speed_kmh', 'engine_rpm', 'throttle_position_percent',
                    'engine_load_percent', 'maf_gs', 'intake_air_temp_c',
                    'acceleration_ms2', 'gear_position']
        X     = df[features]
        y_reg = df['fuel_consumption_lph']   # real LPH values — no pre-processing needed
        y_clf = df['driving_profile']

        ml_model = AdvancedFuelConsumptionPredictor()
        ml_model.train(X, y_reg, y_clf)
        model_trained = True

        X_train, X_test, y_reg_train, y_reg_test, y_clf_train, y_clf_test = (
            train_test_split(X, y_reg, y_clf, test_size=0.2, random_state=42)
        )
        X_test_scaled = ml_model.scaler.transform(X_test)
        log_pred  = ml_model.regressor.predict(X_test_scaled)
        log_true  = np.log1p(y_reg_test)
        clf_pred  = ml_model.classifier.predict(X_test_scaled)

        mae      = mean_absolute_error(log_true, log_pred)
        accuracy = accuracy_score(y_clf_test, clf_pred)

        request.session['training_accuracy'] = round(accuracy * 100, 2)
        request.session['training_mae']      = round(mae, 4)
        request.session['algorithm_reg']     = "Random Forest Regressor"
        request.session['algorithm_clf']     = "Random Forest Classifier"

        messages.success(request, '✅ Model trained successfully!')
        messages.success(request, f'📊 Classification Accuracy: {accuracy:.2%}')
        messages.success(request, f'📈 Regression MAE (log scale): {mae:.4f}')
        messages.success(request, '🤖 Algorithms: Random Forest Ensemble')

    except Exception as e:
        messages.error(request, f'Error training model: {str(e)}')

    return render(request, 'train_model.html')


def estimate_fuel_lph(speed, rpm, throttle, load, acceleration, gear_position):
    """Physics-based LPH fallback (1.5 – 15.0 LPH, always varying)."""
    t = max(0.0, min(throttle / 100.0, 1.0))
    l = max(0.0, min(load     / 100.0, 1.0))
    r = max(0.0, min(rpm      / 7000.0, 1.0))
    s = max(0.0, min(speed    / 200.0,  1.0))
    a = max(0.0, min(abs(acceleration) / 5.0, 1.0))
    g = max(1, min(int(gear_position), 6))

    fuel_demand = (
        t * 0.30 +
        l * 0.25 +
        r * 0.20 +
        s * 0.15 +
        a * 0.07 +
        (1.0 - g / 6.0) * 0.03
    )
    lph = 1.5 + fuel_demand * 13.5
    return round(max(1.5, min(lph, 15.0)), 2)


@login_required
def predict_fuel(request):
    global ml_model, model_trained

    prediction_result = None
    graph_data = None

    if request.method == 'POST':
        try:
            vehicle_speed     = float(request.POST['vehicle_speed'])
            engine_rpm        = float(request.POST['engine_rpm'])
            throttle_position = float(request.POST['throttle_position'])
            engine_load       = float(request.POST['engine_load'])
            maf               = float(request.POST.get('maf', 25.0))
            intake_air_temp   = float(request.POST.get('intake_air_temp', 35.0))
            acceleration      = float(request.POST['acceleration'])
            gear_position     = int(request.POST['gear_position'])

            # ── Fuel consumption prediction ───────────────────────────────
            if model_trained:
                input_data = pd.DataFrame([[
                    vehicle_speed, engine_rpm, throttle_position, engine_load,
                    maf, intake_air_temp, acceleration, gear_position
                ]], columns=['vehicle_speed_kmh', 'engine_rpm',
                             'throttle_position_percent', 'engine_load_percent',
                             'maf_gs', 'intake_air_temp_c',
                             'acceleration_ms2', 'gear_position'])
                fuel_consumption, _ = ml_model.predict(input_data)
            else:
                fuel_consumption = estimate_fuel_lph(
                    vehicle_speed, engine_rpm, throttle_position,
                    engine_load, acceleration, gear_position
                )

            # ── Driving profile — from highest score in calc_profile_scores ──
            # This is the SINGLE source of truth for driving profile.
            # Both the declared label AND Chart 3 use this same dict
            # so they always agree with each other.
            profile_scores  = calc_profile_scores(
                vehicle_speed, engine_rpm, throttle_position,
                engine_load, acceleration, gear_position
            )
            # Declared driving profile = profile with the highest score
            driving_profile = max(profile_scores, key=profile_scores.get)

            # ── Fuel category ─────────────────────────────────────────────
            if fuel_consumption < 4.0:
                fuel_category  = "Very Low";  category_color = "#059669"
            elif fuel_consumption < 6.5:
                fuel_category  = "Low";       category_color = "#10B981"
            elif fuel_consumption < 9.0:
                fuel_category  = "Medium";    category_color = "#F59E0B"
            elif fuel_consumption < 12.0:
                fuel_category  = "High";      category_color = "#EF4444"
            else:
                fuel_category  = "Very High"; category_color = "#DC2626"

            print(f"📊 PREDICTION SUMMARY:")
            print(f"   Fuel : {fuel_consumption:.2f} LPH  ({fuel_category})")
            print(f"   Load : {engine_load:.0f}%")
            print(f"   Profile scores : {profile_scores}")
            print(f"   Declared profile : {driving_profile}")

            graph_data = create_prediction_graph(
                vehicle_speed, engine_rpm, throttle_position, engine_load,
                fuel_consumption, fuel_category, driving_profile,
                acceleration, gear_position, profile_scores
            )

            coolant_temp       = min(100, max(70, intake_air_temp + 50))
            fuel_rail_pressure = 350.0
            brake_pedal_status = False

            ecu_data = ECUData.objects.create(
                vehicle_speed=vehicle_speed,
                engine_rpm=engine_rpm,
                throttle_position=throttle_position,
                engine_load=engine_load,
                maf=maf,
                intake_air_temp=intake_air_temp,
                coolant_temp=coolant_temp,
                fuel_rail_pressure=fuel_rail_pressure,
                acceleration=acceleration,
                brake_pedal_status=brake_pedal_status,
                gear_position=gear_position,
                predicted_fuel_consumption=fuel_consumption,
                fuel_consumption_category=fuel_category,
                driving_profile=driving_profile,
                confidence_score=85.0
            )

            PredictionResult.objects.create(
                user=request.user,
                ecu_data=ecu_data,
                graph_image=graph_data
            )

            prediction_result = {
                'fuel_consumption':    round(fuel_consumption, 2),
                'fuel_category':       fuel_category,
                'category_color':      category_color,
                'driving_profile':     driving_profile,
                'graph_data':          graph_data,
                'engine_load_display': f'{engine_load:.0f}%',
                'engine_load_raw':     engine_load,
            }

        except Exception as e:
            messages.error(request, f'Prediction error: {str(e)}')

    return render(request, 'predict.html', {'prediction_result': prediction_result})


def create_prediction_graph(speed, rpm, throttle, load, fuel, category, profile,
                             acceleration=1.0, gear_position=3, profile_scores=None):
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import io, base64

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Fuel Consumption Analysis', fontsize=16, fontweight='bold')

    # ── Shared helper for Chart 1 and Chart 4 ────────────────────────
    def draw_param_bars(ax, title, include_accel=False):
        if include_accel:
            labels = ['Speed', 'RPM', 'Throttle', 'Load (%)', 'Acceleration']
            values = [
                min(speed             / 200,  1.0) * 100,
                min(rpm               / 7000, 1.0) * 100,
                min(throttle          / 100,  1.0) * 100,
                min(load              / 100,  1.0) * 100,
                min(abs(acceleration) / 5.0,  1.0) * 100,
            ]
            annotations = [
                f'{speed:.0f} km/h',
                f'{rpm:.0f} RPM',
                f'{throttle:.0f}%',
                f'{load:.0f}%',
                f'{abs(acceleration):.1f} m/s²',
            ]
            colors   = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#F59E0B']
            load_idx = 3
        else:
            labels = ['Speed', 'RPM', 'Throttle', 'Load (%)']
            values = [
                min(speed    / 200,  1.0) * 100,
                min(rpm      / 7000, 1.0) * 100,
                min(throttle / 100,  1.0) * 100,
                min(load     / 100,  1.0) * 100,
            ]
            annotations = [
                f'{speed:.0f} km/h',
                f'{rpm:.0f} RPM',
                f'{throttle:.0f}%',
                f'{load:.0f}%',
            ]
            colors   = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
            load_idx = 3

        bars = ax.barh(labels, values, color=colors)
        for i, (bar, note) in enumerate(zip(bars, annotations)):
            ax.text(
                bar.get_width() + 1.5,
                bar.get_y() + bar.get_height() / 2,
                note,
                va='center', ha='left', fontsize=8, fontweight='bold',
                color='#0369A1' if i == load_idx else '#1F2937'
            )
        ax.set_xlim(0, 125)
        ax.set_xticks([0, 25, 50, 75, 100])
        ax.set_xticklabels(['0%', '25%', '50%', '75%', '100%'], fontsize=8)
        ax.set_xlabel('Percentage of Maximum Value (%)', fontsize=8)
        ax.set_title(title)
        ax.grid(True, alpha=0.3, axis='x')

    # ── Chart 1 — Input Parameters ────────────────────────────────────
    draw_param_bars(ax1, 'Input Parameters', include_accel=False)

    # ── Chart 2 — Fuel Consumption Zone ──────────────────────────────
    zones = [
        ('Very Low',  1.5,  4.0,  '#059669'),
        ('Low',       4.0,  6.5,  '#10B981'),
        ('Medium',    6.5,  9.0,  '#F59E0B'),
        ('High',      9.0, 12.0,  '#EF4444'),
        ('Very High', 12.0, 15.0, '#DC2626'),
    ]
    your_fuel  = max(1.5, min(float(fuel), 15.0))
    bar_y      = 0.0
    bar_height = 0.5

    for label, start, end, color in zones:
        ax2.barh(bar_y, end - start, left=start, height=bar_height,
                 color=color, alpha=0.85, edgecolor='white', linewidth=1.5)
        ax2.text((start + end) / 2, bar_y, label,
                 ha='center', va='center', fontsize=8,
                 fontweight='bold', color='white')

    ax2.axvline(x=your_fuel, color='black', linewidth=3, linestyle='--', zorder=5)
    text_ha = 'left' if your_fuel < 12.5 else 'right'
    text_x  = your_fuel + 0.1 if text_ha == 'left' else your_fuel - 0.1
    ax2.text(text_x, bar_y + bar_height * 0.75,
             f'Your: {your_fuel:.1f} LPH',
             va='center', ha=text_ha, fontsize=9,
             fontweight='bold', color='black', zorder=6)

    ax2.set_xlim(1.5, 15.0)
    ax2.set_ylim(-0.5, 1.0)
    ax2.set_xlabel('Fuel Consumption (LPH)')
    ax2.set_title('Fuel Consumption Zone')
    ax2.set_yticks([])
    ax2.grid(True, alpha=0.3, axis='x')
    legend_patches = [mpatches.Patch(color=c, label=f'{l} ({s}–{e} LPH)')
                      for l, s, e, c in zones]
    ax2.legend(handles=legend_patches, loc='lower right', fontsize=7, framealpha=0.8)

    # ── Chart 3 — Driving Profile Distribution (clean pie chart) ─────
    if profile_scores is None:
        profile_scores = {
            'Aggressive': 10, 'Eco-Friendly': 10,
            'City': 10, 'Highway': 10, 'Moderate': 60
        }

    order = ['Aggressive', 'Eco-Friendly', 'City', 'Highway', 'Moderate']

    profile_color_map = {
        'Aggressive':   '#FF2D2D',
        'Eco-Friendly': '#00E676',
        'City':         '#FFD600',
        'Highway':      '#00B0FF',
        'Moderate':     '#D500F9',
    }

    raw_scores = [max(profile_scores.get(p, 0), 1) for p in order]
    total      = sum(raw_scores) or 1
    pct_scores = [s / total * 100 for s in raw_scores]

    pie_colors  = [profile_color_map[p] for p in order]
    explode     = [0.12 if p == profile else 0.03 for p in order]
    wedge_props = dict(linewidth=2.5, edgecolor='white')

    wedges, texts, autotexts = ax3.pie(
        pct_scores,
        labels=None,
        colors=pie_colors,
        explode=explode,
        autopct=lambda pct: f'{pct:.0f}%' if pct >= 7 else '',
        pctdistance=0.72,
        startangle=90,
        wedgeprops=wedge_props,
        textprops=dict(fontsize=8),
        shadow=True,
    )

    for wedge in wedges:
        wedge.set_alpha(1.0)

    dom_idx = order.index(profile)
    for i, at in enumerate(autotexts):
        at.set_color('white')
        if i == dom_idx:
            at.set_fontsize(10)
            at.set_fontweight('bold')
        else:
            at.set_fontsize(8)
            at.set_fontweight('semibold')

    legend_labels = [
        f'★ {p}' if p == profile else f'  {p}'
        for p in order
    ]
    ax3.legend(
        wedges, legend_labels,
        loc='lower center',
        bbox_to_anchor=(0.5, -0.20),
        ncol=2,
        fontsize=7.5,
        framealpha=0.0,
        handlelength=1.4,
        handleheight=1.0,
    )

    ax3.set_title(
        f'Driving Profile  |  Detected: {profile}',
        fontsize=9, fontweight='bold', pad=8
    )

    # ── Chart 4 — Parameter Impact ────────────────────────────────────
    draw_param_bars(ax4, 'Parameter Impact', include_accel=True)

    plt.tight_layout()
    buffer    = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()
    return base64.b64encode(image_png).decode('utf-8')


@login_required
def view_predictions_user(request):
    predictions = PredictionResult.objects.filter(
        user=request.user).order_by('-prediction_date')
    return render(request, 'view_predictions_user.html',
                  {'predictions': predictions})


def view_predictions_admin(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    predictions = PredictionResult.objects.all().order_by('-prediction_date')
    return render(request, 'view_predictions_admin.html',
                  {'predictions': predictions})


def view_users(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    users         = User.objects.all()
    user_profiles = UserProfile.objects.all()
    return render(request, 'view_users.html',
                  {'users': users, 'user_profiles': user_profiles})


def about_us(request):
    return render(request, 'about_us.html')


@login_required
def user_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    return render(request, 'user_profile.html', {'profile': profile})


def logout_view(request):
    if request.session.get('admin_logged_in'):
        request.session.flush()
    else:
        logout(request)
    return redirect('home')