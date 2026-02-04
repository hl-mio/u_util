package com.example.demo.u_util.core;

import org.springframework.beans.BeansException;
import org.springframework.beans.factory.BeanFactory;
import org.springframework.beans.factory.BeanFactoryAware;
import org.springframework.beans.factory.config.ConfigurableListableBeanFactory;
import org.springframework.beans.factory.config.InstantiationAwareBeanPostProcessor;
import org.springframework.context.annotation.Configuration;


@Configuration
public class _bean生命周期控制 implements BeanFactoryAware, InstantiationAwareBeanPostProcessor {
    private ConfigurableListableBeanFactory beanFactory;
    private Boolean flag = true;

    public _bean生命周期控制(){
//        System.out.println("** Bean生命周期控制");
    }

    @Override
    public void setBeanFactory(BeanFactory beanFactory) {
        this.beanFactory = (ConfigurableListableBeanFactory) beanFactory;

        // 通过主动调用beanFactory#getBean来显示实例化目标bean
//        this.beanFactory.getBean(优先加载某些bean.class);
    }

    @Override
    public boolean postProcessAfterInstantiation(Object bean, String beanName) throws BeansException {
        // 通过setBeanFactory方法优先加载的那几个类，没有进入这个方法
        // 通过这个方法来优先加载，相对好点
//        System.out.println(" ---- " + beanName);
//        if (beanName.endsWith("pplication")){
        if (flag){
            flag = false;
//            System.out.println("开始优先加载bean");
            beanFactory.getBean(_优先加载某些bean.class);
        }
        return true;
    }

}