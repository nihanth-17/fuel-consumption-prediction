package com.fuelnet.service;
import org.springframework.stereotype.Service;
import java.util.*;
/** Server-side SVG chart replacement for matplotlib's prediction graph. */
@Service public class ChartService {
 public String profileChart(Map<String,Double> values,String detected,double fuel){StringBuilder b=new StringBuilder("<svg xmlns='http://www.w3.org/2000/svg' width='700' height='280' viewBox='0 0 700 280'><rect width='100%' height='100%' fill='white'/><text x='20' y='28' font-size='20'>Fuel Consumption Analysis: ").append(fuel).append(" LPH</text>");int y=60;for(var e:values.entrySet()){double v=Math.min(100,e.getValue());String c=e.getKey().equals(detected)?"#0369a1":"#94a3b8";b.append("<text x='20' y='").append(y+16).append("' font-size='14'>").append(e.getKey()).append("</text><rect x='170' y='").append(y).append("' width='").append(v*4).append("' height='22' fill='").append(c).append("'/><text x='").append(180+v*4).append("' y='").append(y+16).append("' font-size='12'>").append(String.format(Locale.US,"%.1f%%",v)).append("</text>");y+=38;}return b.append("</svg>").toString();}
}
