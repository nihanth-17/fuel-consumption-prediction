package com.fuelnet.service;
import org.springframework.stereotype.Service;
import weka.classifiers.trees.RandomForest;
import weka.core.*;
import weka.core.converters.CSVLoader;
import java.io.*;
import java.util.*;

/** Java/Weka equivalent of AdvancedFuelConsumptionPredictor in views.py. */
@Service public class RandomForestModelService {
 private static final String[] FEATURES={"vehicle_speed_kmh","engine_rpm","throttle_position_percent","engine_load_percent","maf_gs","intake_air_temp_c","acceleration_ms2","gear_position"};
 private RandomForest fuelModel, profileModel; private Instances fuelHeader, profileHeader; private boolean trained;
 public synchronized Map<String,Object> train(File csv) throws Exception {
  CSVLoader loader=new CSVLoader();loader.setSource(csv); Instances raw=loader.getDataSet();
  ArrayList<Attribute> attrs=new ArrayList<>();for(String n:FEATURES)attrs.add(raw.attribute(n));
  Attribute fuel=raw.attribute("fuel_consumption_lph"), profile=raw.attribute("driving_profile"); if(fuel==null||profile==null)throw new IllegalArgumentException("CSV must include fuel_consumption_lph and driving_profile");
  ArrayList<String> profiles=new ArrayList<>();for(int i=0;i<profile.numValues();i++)profiles.add(profile.value(i)); if(profiles.isEmpty()){Set<String>s=new TreeSet<>();for(Instance x:raw)s.add(x.stringValue(profile));profiles.addAll(s);}
  fuelHeader=new Instances("fuel",new ArrayList<>(attrs),raw.numInstances());fuelHeader.insertAttributeAt(new Attribute("fuel_log"),FEATURES.length);
  profileHeader=new Instances("profile",new ArrayList<>(attrs),raw.numInstances());profileHeader.insertAttributeAt(new Attribute("driving_profile",profiles),FEATURES.length);
  for(Instance x:raw){double[] v=new double[FEATURES.length+1];for(int i=0;i<FEATURES.length;i++)v[i]=x.value(raw.attribute(FEATURES[i]));v[FEATURES.length]=Math.log1p(x.value(fuel));fuelHeader.add(new DenseInstance(1,v));v[FEATURES.length]=profiles.indexOf(x.stringValue(profile));profileHeader.add(new DenseInstance(1,v));}
  fuelHeader.setClassIndex(FEATURES.length);profileHeader.setClassIndex(FEATURES.length);fuelModel=new RandomForest();fuelModel.setNumIterations(200);fuelModel.setSeed(42);fuelModel.buildClassifier(fuelHeader);profileModel=new RandomForest();profileModel.setNumIterations(200);profileModel.setSeed(42);profileModel.buildClassifier(profileHeader);trained=true;
  return Map.of("trained",true,"samples",raw.numInstances(),"regressor","Weka RandomForest","classifier","Weka RandomForest");
 }
 public synchronized Optional<Result> predict(FuelPredictionService.Input x) throws Exception {if(!trained)return Optional.empty();double[] v={x.vehicleSpeed(),x.engineRpm(),x.throttlePosition(),x.engineLoad(),x.maf(),x.intakeAirTemp(),x.acceleration(),x.gearPosition(),0};Instance a=new DenseInstance(1,v);a.setDataset(fuelHeader);double fuel=Math.max(1.5,Math.min(15,Math.expm1(fuelModel.classifyInstance(a))));a.setDataset(profileHeader);String p=profileHeader.classAttribute().value((int)profileModel.classifyInstance(a));return Optional.of(new Result(Math.round(fuel*100d)/100d,p));}
 public record Result(double fuel,String profile){}
}
