package com.fuelnet.web;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
@Controller public class PageController {
 @GetMapping({"/","/home"}) String home(){return "home";}
 @GetMapping("/about") String about(){return "about";}
 @GetMapping("/register") String register(){return "register";}
 @GetMapping("/user-login") String userLogin(){return "user-login";}
 @GetMapping("/user-dashboard") String userDashboard(){return "user-dashboard";}
 @GetMapping("/user-profile") String userProfile(){return "user-profile";}
 @GetMapping("/predict-fuel") String predict(){return "predict";}
 @GetMapping("/view-predictions-user") String userPredictions(){return "view-predictions-user";}
 @GetMapping("/admin-login") String adminLogin(){return "admin-login";}
 @GetMapping("/admin-dashboard") String adminDashboard(){return "admin-dashboard";}
 @GetMapping("/upload-dataset") String upload(){return "upload-dataset";}
 @GetMapping("/train-model") String train(){return "train-model";}
 @GetMapping("/view-users") String users(){return "view-users";}
 @GetMapping("/view-predictions-admin") String adminPredictions(){return "view-predictions-admin";}
}
