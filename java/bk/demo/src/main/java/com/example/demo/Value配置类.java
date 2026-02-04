package com.example.demo;

import lombok.Data;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

import java.util.List;


@Data
@Configuration
public class Value配置类 {
    @Value("${my.conf.状态码数组2:}")
    List<Integer> 状态码数组;

    @Value("${my.conf.是否启用某配置}")
    Boolean 是否启用某配置;
}
