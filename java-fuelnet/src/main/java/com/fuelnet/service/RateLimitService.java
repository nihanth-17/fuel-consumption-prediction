package com.fuelnet.service;
import org.springframework.stereotype.Service;
import java.time.*;import java.util.concurrent.*;
/** Sliding fixed-window limiter suitable for one instance; use Redis for a multi-node deployment. */
@Service public class RateLimitService {private final ConcurrentHashMap<String,State> states=new ConcurrentHashMap<>();private record State(Instant started,int count){} public boolean allowed(String key,int limit,Duration period){Instant n=Instant.now();return states.compute(key,(k,s)->s==null||n.isAfter(s.started.plus(period))?new State(n,1):new State(s.started,s.count+1)).count<=limit;}}
