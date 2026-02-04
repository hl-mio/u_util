package com.example.demo;

import lombok.Data;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

import java.util.List;
import java.util.Map;


@Data
@Configuration
@ConfigurationProperties(
        prefix = "my.conf",             // 变量前缀 或者说 命名空间
        ignoreInvalidFields = false,    // 是否无视掉，解析出错的配置文件字段。不无视会怎么样？报错
        ignoreUnknownFields = true      // 是否无视掉，class文件里少写的字段
)
public class 属性配置类 {
    String ip;
    Integer port;
    List<Integer> list;
    Map<String,String> dict;
}
