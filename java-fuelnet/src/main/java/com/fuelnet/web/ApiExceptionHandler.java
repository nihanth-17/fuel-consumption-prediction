package com.fuelnet.web;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import java.time.Instant;
import java.util.*;
@RestControllerAdvice public class ApiExceptionHandler {
 @ExceptionHandler({IllegalArgumentException.class,org.springframework.web.bind.MethodArgumentNotValidException.class})
 ResponseEntity<?> badRequest(Exception e){return error(HttpStatus.BAD_REQUEST,e.getMessage());}
 @ExceptionHandler(Exception.class) ResponseEntity<?> unknown(Exception e){return error(HttpStatus.INTERNAL_SERVER_ERROR,"Unexpected server error");}
 private ResponseEntity<?> error(HttpStatus s,String m){return ResponseEntity.status(s).body(Map.of("timestamp",Instant.now(),"status",s.value(),"error",m==null?"Invalid request":m));}
}
