package com.example.demo.u_util.to;


import cn.hutool.core.util.IdUtil;
import cn.hutool.core.util.ObjectUtil;
import cn.hutool.core.util.StrUtil;
import cn.hutool.crypto.SecureUtil;

import static com.example.demo.u_util.to.to_json.to_json_str;

public class to_x {

    // 全部都是随机uuid
    public static String to_uuid() {
        return to_uuid(true);
    }
    // 全部都是随机uuid
    public static String to_uuid(Boolean 去除中横线) {
        if(去除中横线) return IdUtil.fastSimpleUUID();

        return IdUtil.fastUUID();
    }


    public static String to_md5(String data) {
        return SecureUtil.md5(data);
    }
    public static String to_md5(byte[] bytes, String charset) {
        String data = StrUtil.str(bytes,charset);
        return to_md5(data);
    }
    public static String to_md5(Byte[] bytes, String charset) {
        String data = StrUtil.str(bytes,charset);
        return to_md5(data);
    }


    public static <T> T to_self(T obj) {
        return to_self_by_json(obj);
//        需要对应obj的类 extends CloneSupport
//        return ObjectUtil.clone(obj);
    }
    public static <T> T to_self_by_json(T obj) {
        String jsonStr = to_json.to_json_str(obj);
        return (T) to_json.to_json_obj(jsonStr, obj.getClass());
    }

}
