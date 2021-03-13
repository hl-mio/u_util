package com.example.demo.u_util.other;

public class other {

    public static int get_obj_id(Object obj) {
        return java.lang.System.identityHashCode(obj);
    }

    public static int get对象唯一标识符(Object obj) {
        return System.identityHashCode(obj);
    }

}
