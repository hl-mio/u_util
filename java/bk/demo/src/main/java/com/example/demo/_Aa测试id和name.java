package com.example.demo;

import org.springframework.beans.factory.BeanNameAware;
import org.springframework.stereotype.Component;

@Component()
public class _Aa测试id和name implements BeanNameAware {

    @Override
    public void setBeanName(String name) {
        System.out.println("外部的name: "+name);
    }
}
