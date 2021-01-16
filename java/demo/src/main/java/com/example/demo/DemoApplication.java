package com.example.demo;

import cn.hutool.json.JSONUtil;
import com.example.demo.test.User;
import com.example.demo.u_util.core.app;
import com.example.demo.u_util.other.other;
import com.example.demo.u_util.to.Convert;
import com.example.demo.u_util.to.change;
import com.example.demo.u_util.to.*;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;


@SpringBootApplication
public class DemoApplication {

    public static void main(String[] args) {
        ConfigurableApplicationContext context = SpringApplication.run(DemoApplication.class, args);

        属性配置类 配置 = app.getBean(属性配置类.class);

        System.out.println();
        System.out.println(配置.ip);
        System.out.println(配置.port);
        System.out.println(配置.list);
        System.out.println(配置.dict);

        System.out.println("获取的context：");
        System.out.println(app.applicationContext);


        var value配置 = app.getBean(Value配置类.class);
        System.out.println();
        System.out.println(value配置.状态码数组);
        System.out.println(value配置.是否启用某配置);



        var aaa = new User();
        aaa.setId(123L);
        aaa.setName("aaa");
        ObjectMapper mapper = new ObjectMapper();
        try {
            System.out.println(mapper.writeValueAsString(aaa));
        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }
        ;
        System.out.println(to_json.to_json_str(aaa));
        System.out.println();
        System.out.println();

    }

}
