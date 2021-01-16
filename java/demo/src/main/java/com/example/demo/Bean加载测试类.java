package com.example.demo;

import com.example.demo.u_util.core.ApplicationContextUtil;
import org.springframework.stereotype.Component;

@Component
public class Bean加载测试类 {

    public Bean加载测试类(){
        System.out.println("** Bean加载测试类");
        System.out.println("获取的context：");
        System.out.println(ApplicationContextUtil.applicationContext);
    }
}
