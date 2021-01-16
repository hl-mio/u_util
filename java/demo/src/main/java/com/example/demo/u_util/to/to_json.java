package com.example.demo.u_util.to;

import cn.hutool.json.JSON;
import cn.hutool.json.JSONArray;
import cn.hutool.json.JSONObject;
import cn.hutool.json.JSONUtil;

import java.util.List;

public class to_json {

    public static JSON to_json(Object obj) {
        return JSONUtil.parse(obj);
    }
    public static JSONObject to_json_obj(Object obj) {
        return (JSONObject)to_json(obj);
    }
    public static JSONArray to_json_arr(Object obj) {
        return (JSONArray)to_json(obj);
    }
    public static <T> T to_json_obj(Object obj, Class<T> beanClass) {
        JSONObject jsonObj = to_json_obj(obj);
        return JSONUtil.toBean(jsonObj, beanClass);
    }
    public static <T> List<T> to_json_arr(Object obj, Class<T> beanClass) {
        JSONArray jsonArr = to_json_arr(obj);
        return JSONUtil.toList(jsonArr, beanClass);
    }


    public static String to_json_str(Object obj, int 缩进几个空格) {
        JSON json = to_json(obj);
        return json.toJSONString(缩进几个空格);
    }
    public static String to_json_str(Object obj) {
        return to_json_str(obj,0);
    }
    public static String to_json_str_pretty(Object obj) {
        return to_json_str(obj,4);
    }

}
