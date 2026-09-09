package com.fuelnet.config;

import org.springframework.context.annotation.*;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.csrf.CookieCsrfTokenRepository;

/** Security baseline for the Java port: BCrypt passwords, secure response headers and no default user. */
@Configuration @EnableWebSecurity
public class SecurityConfig {
 @Bean PasswordEncoder passwordEncoder(){ return new BCryptPasswordEncoder(12); }
 @Bean SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
  http.csrf(csrf->csrf.csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse()))
      .headers(headers->headers.contentSecurityPolicy(csp->csp.policyDirectives("default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'")))
      .requiresChannel(channel->channel.anyRequest().requiresSecure())
      .authorizeHttpRequests(a->a.anyRequest().permitAll())
      .httpBasic(b->b.disable()).formLogin(f->f.disable());
  return http.build();
 }
}
