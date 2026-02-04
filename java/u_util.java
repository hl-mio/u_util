// @Time    : 2025-12-29
// @PreTime : 2025-12-29
// @Author  : hlmio
//package xxx;

import cn.afterturn.easypoi.excel.ExcelExportUtil;
import cn.afterturn.easypoi.excel.entity.ExportParams;
import cn.afterturn.easypoi.excel.entity.enmus.ExcelType;
import cn.afterturn.easypoi.excel.entity.params.ExcelExportEntity;
import cn.hutool.core.util.StrUtil;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.fasterxml.jackson.datatype.jsr310.deser.LocalDateTimeDeserializer;
import com.fasterxml.jackson.datatype.jsr310.ser.LocalDateTimeSerializer;
import lombok.SneakyThrows;
import org.apache.poi.ss.usermodel.Workbook;

import javax.servlet.ServletOutputStream;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


/**
 * 模仿u_工具的对应工具类
 *
 */
public class u_util {
    public static final String SQL_COUNT_FIELD_NAME = "page_count";
    public static final String oracle_time_format = "yyyy-MM-dd HH:mm:ss";


    /**
     * 比较笨的过滤sql字符串
     */
    public static String doSQLFilter(String str) {
        //str = str.replaceAll("\\.", "。");
        //str = str.replaceAll(":", "：");
        str = str.replaceAll(";", "；");
        str = str.replaceAll("&", "＆");
        str = str.replaceAll("<", "＜");
        str = str.replaceAll(">", "＞");
        str = str.replaceAll("'", "＇");
        //str = str.replaceAll("\"", "“");
        str = str.replaceAll("--", "－－");
        //str = str.replaceAll("/", "／");
        //str = str.replaceAll("%", "％");
        str = str.replaceAll("\\+", "＋");
        str = str.replaceAll("\\(", "（");
        str = str.replaceAll("\\)", "）");

        str = str.replaceAll(" or ", "");
        str = str.replaceAll(" Or ", "");
        str = str.replaceAll(" oR ", "");
        str = str.replaceAll(" OR ", "");
        return str;
    }



    public static void exportExcel(HttpServletResponse response, List<Map<String, Object>> mapList, List<ExcelExportEntity> entityList) {
        u_util.exportExcel(response, mapList, entityList, "文件" + u_util.to_now_str("yyyyMMddHHmmss") + ".xlsx");
    }
    /**
     * 导出excel
     */
    public static void exportExcel(HttpServletResponse response, List<Map<String, Object>> mapList, List<ExcelExportEntity> entityList, String fileName) {
        // 生成workbook
        try (Workbook workbook = ExcelExportUtil.exportExcel(
                new ExportParams(null, null, ExcelType.XSSF)
                , entityList
                , mapList);
             ServletOutputStream outputStream = response.getOutputStream()) {
            response.setCharacterEncoding("UTF-8");
            response.setHeader("content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
            response.setHeader("Content-Disposition",
                    "attachment;filename=" + URLEncoder.encode(fileName, "UTF-8"));
            workbook.write(outputStream);
            outputStream.flush();
        } catch (Exception e) {
            throw new RuntimeException(e.getMessage());
        }
    }


    /**
     * 获取json字段值
     */
    @SneakyThrows
    public static String getJsonFieldStr(Map<String, Object> json, String key, String defaultStr, boolean isCanEmpty, String errMsg_fieldName) {
        String value;
        try {
            value = json.get(key).toString();
        } catch (Exception e) {
            value = defaultStr;
        }
        // 过滤sql字符
        value = u_util.doSQLFilter(value);

        if (!isCanEmpty && StrUtil.isBlank(value)) {
            String msg = "参数字段不能为空";
            if (!StrUtil.isBlank(errMsg_fieldName)) {
                msg += ": " + errMsg_fieldName;
            } else {
                msg += ": " + key;
            }
            throw new UserTipException(msg);
        }
        return value;
    }


    public static String getJsonFieldStr(Map<String, Object> json, String key) {
        return u_util.getJsonFieldStr(json, key, "", true, "");
    }

    public static int getJsonFieldInt(Map<String, Object> json, String key, int defaultInt) {
        int rst;
        String value = u_util.getJsonFieldStr(json, key);
        if (StrUtil.isEmpty(value)) {
            rst = defaultInt;
        } else {
            try {
                rst = Integer.parseInt(value);
            } catch (Exception e) {
                rst = defaultInt;
            }
        }

        return rst;
    }




    //#region ------sql------
    /**
     * 获取分页sql
     */
    public static String getSql_page_pg(String baseSql, int pageIndex, int pageSize, ArrayList<Object> paramList, String orderByFieldName){
        return getSql_page_pg(baseSql, pageIndex, pageSize, orderByFieldName, paramList);
    }
    /**
     * 获取分页sql
     */
    public static String getSql_page_pg(String baseSql, int pageIndex, int pageSize, String orderByFieldName, ArrayList<Object> paramList){
        int offset = (pageIndex - 1) * pageSize;
        paramList.add(pageSize);
        paramList.add(offset);
        String page_sql = """
            select a.*
            from ( %s ) a
            order by %s  -- 分页必须有明确的排序
            limit ? offset ?
        """;
        return String.format(page_sql, baseSql, orderByFieldName);
    }
    /**
     * 获取分页sql
     */
    public static String getSql_page_pg(String baseSql, int pageIndex, int pageSize, String orderByFieldName){
        int offset = (pageIndex - 1) * pageSize;
        String page_sql = """
            select a.*
            from ( %s ) a
            order by %s  -- 分页必须有明确的排序
            limit %s offset %s
        """;
        return String.format(page_sql, baseSql, orderByFieldName, pageSize, offset);
    }

    /**
     * 获取分页sql，用于oracle
     */
    public static String getSql_page(String baseSql, int pageIndex, int pageSize, ArrayList<Object> paramList){
        int pageLow = (pageIndex - 1) * pageSize;
        int pageHigh = pageIndex * pageSize;
        paramList.add(pageHigh);
        paramList.add(pageLow);
        String page_sql = "" +
                "    SELECT a.*,rownum PAGE_SEQ " +
                "    FROM " +
                "            ( " +
                "                    SELECT A.*, ROWNUM PAGE_RN " +
                "                    FROM " +
                "                            ( " +
                "                                    %s " +
                "                            ) A " +
                "                    WHERE ROWNUM <= ? " +
                "            ) a " +
                "    WHERE PAGE_RN > ? " +
                "";
        return String.format(page_sql, baseSql);
    }
    /**
     * 获取分页sql，用于oracle，int是否会带来注入？
     */
    public static String getSql_page(String baseSql, int pageIndex, int pageSize){
        int pageLow = (pageIndex - 1) * pageSize;
        int pageHigh = pageIndex * pageSize;
        String page_sql = "" +
                "    SELECT a.*,rownum PAGE_SEQ " +
                "    FROM " +
                "            ( " +
                "                    SELECT A.*, ROWNUM PAGE_RN " +
                "                    FROM " +
                "                            ( " +
                "                                    %s " +
                "                            ) A " +
                "                    WHERE ROWNUM <= %s " +
                "            ) a " +
                "    WHERE PAGE_RN > %s " +
                "";
        return String.format(page_sql, baseSql, pageHigh, pageLow);
    }
    public static String getSql_count(String baseSql){
        String count_sql = " SELECT count(*) as " + u_util.SQL_COUNT_FIELD_NAME + " FROM ( %s ) a ";
        return String.format(count_sql, baseSql);
    }
    //#endregion ======sql======

    //#region ------7.to_xxx------

    //#region 未分类

    /**
     * 【静态函数】对字符串进行Base64URL编码（无填充，UTF-8字符集）
     * @param str 原始字符串（可为null/空）
     * @return Base64URL编码后的字符串，null/空输入返回空字符串
     */
    public static String from_str_to_base64UrlStr(String str){
        // 空值处理，避免空指针
        if (str == null || str.trim().isEmpty()) {
            return "";
        }
        // 转换为字节数组并编码
        byte[] originalBytes = str.getBytes(StandardCharsets.UTF_8);

        // 空值处理
        if (originalBytes == null || originalBytes.length == 0) {
            return "";
        }
        // 获取URL安全编码器（无填充模式，适配JWT等场景）
        Base64.Encoder urlEncoder = Base64.getUrlEncoder().withoutPadding();
        return urlEncoder.encodeToString(originalBytes);
    }
    /**
     * 【静态函数】将Base64URL字符串解码为原始字符串（UTF-8字符集）
     * @param base64UrlStr Base64URL编码字符串（可为null/空）
     * @return 解码后的原始字符串，null/空输入返回空字符串
     */
    public static String from_base64UrlStr_to_str(String base64UrlStr) {
        // 空值处理
        if (base64UrlStr == null || base64UrlStr.trim().isEmpty()) {
            return "";
        }
        // 先解码为字节数组，再转换为字符串
        // 获取URL安全解码器，自动兼容无填充/带填充格式
        Base64.Decoder urlDecoder = Base64.getUrlDecoder();
        byte[] decodedBytes = urlDecoder.decode(base64UrlStr);
        return new String(decodedBytes, StandardCharsets.UTF_8);
    }

    //#endregion

    //#region json

    // 全局 ObjectMapper 实例
    private static final ObjectMapper objectMapper;
    // 静态代码块：初始化并配置 ObjectMapper（类加载时执行，仅执行一次）
    static {
        // 1. 初始化 ObjectMapper 实例
        objectMapper = new ObjectMapper();

        // 2. 核心配置 - 时区
        objectMapper.setTimeZone(TimeZone.getTimeZone("GMT+8"));

        // 3. 序列化配置
        // 忽略 null 字段
        //objectMapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
        // 禁止空 POJO 序列化报错
        objectMapper.disable(SerializationFeature.FAIL_ON_EMPTY_BEANS);
        // 日期不序列化为时间戳
        objectMapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);

        // 4. 反序列化配置
        // 忽略未知字段
        objectMapper.disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);
        // 空字符串转为 null
        objectMapper.enable(DeserializationFeature.ACCEPT_EMPTY_STRING_AS_NULL_OBJECT);
        // 反序列化：当 JSON 中的枚举值在 Java Enum 中不存在时，不抛异常，直接反序列化为 null
        // 适用于前端 / 第三方接口枚举值不可控的场景
        objectMapper.enable(DeserializationFeature.READ_UNKNOWN_ENUM_VALUES_AS_NULL);
        // 反序列化：将 JSON 中的浮点数反序列化为 BigDecimal，而不是 Double
        // 避免浮点精度丢失，适用于金额、计费、报表等场景
        objectMapper.enable(DeserializationFeature.USE_BIG_DECIMAL_FOR_FLOATS);

        // 5. 处理 Java 8 日期类型（LocalDateTime）
        JavaTimeModule javaTimeModule = new JavaTimeModule();
        DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        javaTimeModule.addSerializer(LocalDateTime.class, new LocalDateTimeSerializer(dateTimeFormatter));
        javaTimeModule.addDeserializer(LocalDateTime.class, new LocalDateTimeDeserializer(dateTimeFormatter));
        objectMapper.registerModule(javaTimeModule);

        // 6. 扩展点：注册自定义序列化/反序列化模块
        // SimpleModule customModule = new SimpleModule();
        // customModule.addSerializer(CustomClass.class, new CustomClassSerializer());
        // OBJECT_MAPPER.registerModule(customModule);
    }

    /**
     * 按路径取 int 值
     * @param jsonStr json字符串
     * @param fieldPath 取值路径
     * @param defaultValue 默认值
     * @return 取到的 int 值，路径不存在或类型不匹配返回默认值
     */
    public static int get_json_int(String jsonStr, String fieldPath, int defaultValue) {
        try {
            String str = get_json_str(jsonStr, fieldPath);
            return Integer.parseInt(str);
        } catch (NumberFormatException e) {
            return defaultValue;
        }
    }
    /**
     * 按路径取 字符串 值
     * @param fieldPath 取数的path，比如：a.b[2].c 、 a.b.2.c 、 a/b/2/c
     * @return 取到的 字符串 值，路径不存在或类型不匹配返回""
     */
    public static String get_json_str(Map<String, Object> json, String fieldPath) {
        String jsonStr = u_util.to_json_str(json);
        return get_json_str(jsonStr, fieldPath);
    }
    /**
     * 按路径取 字符串 值
     * @param fieldPath 取数的path，比如：a.b[2].c 、 a.b.2.c 、 a/b/2/c
     * @return 取到的 字符串 值，路径不存在或类型不匹配返回""
     */
    public static String get_json_str(String jsonStr, String fieldPath) {
        JsonNode json = u_util.to_json_any(jsonStr);
        return get_json_str(json, fieldPath);
    }
    /**
     * 按路径取 字符串 值
     * @param fieldPath 取数的path，比如：a.b[2].c 、 a.b.2.c 、 a/b/2/c
     * @return 取到的 字符串 值，路径不存在或类型不匹配返回""
     */
    public static String get_json_str(JsonNode json, String fieldPath) {
        String rst;
        String err_rst = "";

        if (json == null || fieldPath == null || fieldPath.trim().isEmpty()) {
            rst = err_rst;
            return rst;
        }

        String jsonPointerPath = fieldPath
                .replace("[", "/")
                .replace("]", "")
                .replace(".", "/");

        if (!jsonPointerPath.startsWith("/")) {
            jsonPointerPath = "/" + jsonPointerPath;
        }

        JsonNode node = json.at(jsonPointerPath);

        if (node.isMissingNode() || node.isNull()) {
            rst = err_rst;
            return rst;
        }

        if (node.isValueNode()) {
            rst = node.asText();
        } else {
            rst =  node.toString();
        }

        return rst;
    }
    public static JsonNode to_json_any(String jsonStr) {
        if (jsonStr == null || jsonStr.trim().isEmpty()) {
            return null;
        }
        //ObjectMapper objectMapper = new ObjectMapper();
        try {
            return objectMapper.readTree(jsonStr);
        } catch (IOException e) {
            return null;
        }
    }
    public static <T> List<T> to_json_list(String jsonStr, Class<T> clazz) {
        if (jsonStr == null || jsonStr.trim().isEmpty()) {
            return null;
        }
        //ObjectMapper objectMapper = new ObjectMapper();
        //objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);

        try {
            return objectMapper.readValue(
                    jsonStr,
                    objectMapper.getTypeFactory().constructCollectionType(List.class, clazz)
            );
        } catch (IOException e) {
            return null;
        }
    }
    public static <T> T to_json_obj(String jsonStr, Class<T> clazz){
        if (jsonStr == null || jsonStr.trim().isEmpty()) {
            return null;
        }
        //ObjectMapper objectMapper = new ObjectMapper();
        //// 忽略未知字段
        //objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);

        try {
            return objectMapper.readValue(jsonStr, clazz);
        } catch (IOException e) {
            return null;
        }
    }
    public static String to_json_str(Object obj){
        // 创建 ObjectMapper 对象
        //ObjectMapper objectMapper = new ObjectMapper();
        // 转成 JSON 字符串
        String jsonStr = "";
        try {
            jsonStr = objectMapper.writeValueAsString(obj);
        } catch (JsonProcessingException e) {
        }
        return jsonStr;
    }
    //#endregion

    //#region time  --LocalDateTime是原点，是核心中间类

    // 默认时间格式模板 (Python: %Y-%m-%d %H:%M:%S → Java: yyyy-MM-dd HH:mm:ss)
    private static final String 时间字符串_模板 = "yyyy-MM-dd HH:mm:ss";
    // Oracle 格式到 Java DateTimeFormatter 格式的映射（按长度从长到短排序）
    private static final Map<String, String> ORACLE_TO_JAVA_FORMAT_MAPPING;
    // Oracle 格式特征正则（匹配专属关键词，用于自动识别）
    private static final Pattern ORACLE_FORMAT_PATTERN;
    static {
        ORACLE_TO_JAVA_FORMAT_MAPPING = new HashMap<>();
        // 初始化映射关系，保持和 Python 一致的匹配优先级
        ORACLE_TO_JAVA_FORMAT_MAPPING.put("YYYY", "yyyy");
        ORACLE_TO_JAVA_FORMAT_MAPPING.put("yyyy", "yyyy");
        ORACLE_TO_JAVA_FORMAT_MAPPING.put("MM", "MM");
        ORACLE_TO_JAVA_FORMAT_MAPPING.put("mm", "MM");
        ORACLE_TO_JAVA_FORMAT_MAPPING.put("DD", "dd");
        ORACLE_TO_JAVA_FORMAT_MAPPING.put("dd", "dd");
        ORACLE_TO_JAVA_FORMAT_MAPPING.put("HH24", "HH");
        ORACLE_TO_JAVA_FORMAT_MAPPING.put("hh24", "HH");
        ORACLE_TO_JAVA_FORMAT_MAPPING.put("MI", "mm");
        ORACLE_TO_JAVA_FORMAT_MAPPING.put("mi", "mm");
        ORACLE_TO_JAVA_FORMAT_MAPPING.put("SS", "ss");
        ORACLE_TO_JAVA_FORMAT_MAPPING.put("ss", "ss");
        ORACLE_TO_JAVA_FORMAT_MAPPING.put("FF6", "SSSSSS"); // 6位纳秒（微秒）
        ORACLE_TO_JAVA_FORMAT_MAPPING.put("ff6", "SSSSSS");
        ORACLE_TO_JAVA_FORMAT_MAPPING.put("FF3", "SSS");    // 3位毫秒
        ORACLE_TO_JAVA_FORMAT_MAPPING.put("ff3", "SSS");
        ORACLE_TO_JAVA_FORMAT_MAPPING.put("FF", "SSS");     // 默认3位毫秒
        ORACLE_TO_JAVA_FORMAT_MAPPING.put("ff", "SSS");

        // 初始化Oracle格式特征正则（匹配专属关键词，忽略大小写）
        // 特征：HH24、MI、FF[0-9]?、YYYY（Java格式中不会出现这些）
        String oracleFeatures = "HH24|hh24|MI|mi|FF\\d?|ff\\d?|YYYY";
        ORACLE_FORMAT_PATTERN = Pattern.compile(oracleFeatures);
    }
    /**
     * 自动检测格式字符串是否为Oracle格式
     * @param format_str 格式字符串
     * @return true=Oracle格式，false=Java原生格式
     */
    private static boolean is_oracle_format(String format_str) {
        if (format_str == null || format_str.isEmpty()) {
            return false;
        }
        Matcher matcher = ORACLE_FORMAT_PATTERN.matcher(format_str);
        return matcher.find();
    }
    /**
     * 将 Oracle 时间格式转换为 Java 时间格式（对应 Python: from_oracle_time_format_to_py_time_format）
     * @param format_str Oracle 格式字符串
     * @return Java DateTimeFormatter 兼容的格式字符串
     */
    private static String from_oracle_time_format_to_java_time_format(String format_str) {
        if (format_str == null || format_str.isEmpty()) {
            return 时间字符串_模板;
        }
        // 按最长匹配优先编译正则表达式
        String regex = String.join("|",
                ORACLE_TO_JAVA_FORMAT_MAPPING.keySet().stream()
                        .sorted((a, b) -> Integer.compare(b.length(), a.length()))
                        .toArray(String[]::new)
        );
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(format_str);
        StringBuffer result = new StringBuffer();

        while (matcher.find()) {
            String match = matcher.group();
            matcher.appendReplacement(result, ORACLE_TO_JAVA_FORMAT_MAPPING.get(match));
        }
        matcher.appendTail(result);
        return result.toString();
    }
    /**
     * 获取当前 LocalDateTime
     * @return 当前时间
     */
    private static LocalDateTime get_now_datetime() {
        return LocalDateTime.now();
    }
    /**
     * 转换为 LocalDateTime 对象（对应 Python: to_time_datetime）
     * @param 字符串or时间戳or时间对象 输入对象：String(时间字符串)/Long(时间戳)/LocalDateTime/0(当前时间)
     * @param 格式字符串 格式字符串
     * @param 增加几秒 增加的秒数
     * @param 增加几分钟 增加的分钟数
     * @param 增加几小时 增加的小时数
     * @param 增加几天 增加的天数
     * @return 转换后的 LocalDateTime 对象
     */
    public static LocalDateTime to_time_datetime(
            Object 字符串or时间戳or时间对象,
            String 格式字符串,
            long 增加几秒,
            long 增加几分钟,
            long 增加几小时,
            long 增加几天
    ) {
        boolean 是否由oracle格式转为java格式 = is_oracle_format(格式字符串);
        // 处理格式字符串
        String finalFormat = 格式字符串;
        if (是否由oracle格式转为java格式) {
            finalFormat = from_oracle_time_format_to_java_time_format(finalFormat);
        }

        // 解析输入对象为 LocalDateTime
        LocalDateTime 原点时间;
        Object obj = 字符串or时间戳or时间对象;
        if (obj == null || obj.equals(0)) {
            // 输入为0/null → 返回当前时间
            原点时间 = get_now_datetime();
        } else if (obj instanceof String) {
            // 字符串类型
            String 字符串 = ((String) obj).trim();
            if (字符串.isEmpty() || 字符串.equals("0")) {
                原点时间 = get_now_datetime();
            } else {
                try {
                    原点时间 = LocalDateTime.parse(字符串, DateTimeFormatter.ofPattern(finalFormat));
                } catch (DateTimeParseException e) {
                    throw new IllegalArgumentException("时间字符串解析失败：" + 字符串 + "，格式：" + finalFormat, e);
                }
            }
        } else if (obj instanceof Long) {
            // 时间戳（秒/毫秒）→ Java 时间戳默认是毫秒，兼容秒级时间戳
            long 时间戳 = (Long) obj;
            Instant instant;
            if (时间戳 < 1000000000000L) { // 秒级时间戳（小于13位）
                instant = Instant.ofEpochSecond(时间戳);
            } else { // 毫秒级时间戳
                instant = Instant.ofEpochMilli(时间戳);
            }
            原点时间 = LocalDateTime.ofInstant(instant, ZoneId.systemDefault());
        } else if (obj instanceof LocalDateTime) {
            // 直接是 LocalDateTime 对象
            原点时间 = (LocalDateTime) obj;
        } else {
            throw new IllegalArgumentException("参数类型未支持：" + obj.getClass().getName());
        }

        // 处理时间增减
        LocalDateTime 结果时间 = 原点时间;
        if (增加几天 > 0) {
            结果时间 = 结果时间.plusDays(增加几天);
        }
        if (增加几小时 > 0) {
            结果时间 = 结果时间.plusHours(增加几小时);
        }
        if (增加几分钟 > 0) {
            结果时间 = 结果时间.plusMinutes(增加几分钟);
        }
        if (增加几秒 > 0) {
            结果时间 = 结果时间.plusSeconds(增加几秒);
        }

        return 结果时间;
    }
    // 重载方法：简化参数（默认格式、无增减、默认转换Oracle格式）
    public static LocalDateTime to_time_datetime(Object 字符串or时间戳or时间对象) {
        return to_time_datetime(字符串or时间戳or时间对象, 时间字符串_模板, 0, 0, 0, 0);
    }

    /**
     * 转换为时间字符串（对应 Python: to_time_str）
     * @param datetime_or_字符串or时间戳or时间对象 输入对象：String/Long/LocalDateTime/0
     * @param 格式字符串 输出格式字符串
     * @param 增加几秒 增加秒数
     * @param 增加几分钟 增加分钟数
     * @param 增加几小时 增加小时数
     * @param 增加几天 增加天数
     * @param 格式字符串_旧 解析输入字符串时使用的格式（仅输入为字符串时生效）
     * @return 格式化后的时间字符串
     */
    public static String to_time_str(
            Object datetime_or_字符串or时间戳or时间对象,
            String 格式字符串,
            long 增加几秒,
            long 增加几分钟,
            long 增加几小时,
            long 增加几天,
            String 格式字符串_旧
    ) {
        boolean 是否由oracle格式转为java格式 = is_oracle_format(格式字符串);

        // 处理输入对象为 LocalDateTime
        LocalDateTime 时间对象;
        if (datetime_or_字符串or时间戳or时间对象 instanceof String) {
            时间对象 = to_time_datetime(datetime_or_字符串or时间戳or时间对象, 格式字符串_旧, 增加几秒, 增加几分钟, 增加几小时, 增加几天);
        } else {
            时间对象 = to_time_datetime(datetime_or_字符串or时间戳or时间对象, 格式字符串, 增加几秒, 增加几分钟, 增加几小时, 增加几天);
        }

        // 处理输出格式
        String finalFormat = 格式字符串;
        if (是否由oracle格式转为java格式) {
            finalFormat = from_oracle_time_format_to_java_time_format(finalFormat);
        }
        return 时间对象.format(DateTimeFormatter.ofPattern(finalFormat));
    }
    // 重载方法：简化参数（默认格式、无增减、默认旧格式、默认转换Oracle格式）
    public static String to_time_str(Object datetime_or_字符串or时间戳or时间对象, String 格式字符串) {
        return to_time_str(datetime_or_字符串or时间戳or时间对象, 格式字符串, 0, 0, 0, 0, 时间字符串_模板);
    }

    /**
     * 转换为 Unix 时间戳（秒级，对应 Python: to_time_unix）
     * @param datetime_or_字符串or时间戳or时间对象 输入对象：String/Long/LocalDateTime/0
     * @param 增加几秒 增加秒数
     * @param 增加几分钟 增加分钟数
     * @param 增加几小时 增加小时数
     * @param 增加几天 增加天数
     * @return 秒级时间戳
     */
    public static long to_time_unix(
            Object datetime_or_字符串or时间戳or时间对象,
            long 增加几秒,
            long 增加几分钟,
            long 增加几小时,
            long 增加几天
    ) {
        LocalDateTime 时间对象 = to_time_datetime(datetime_or_字符串or时间戳or时间对象, 时间字符串_模板, 增加几秒, 增加几分钟, 增加几小时, 增加几天);
        // 转换为秒级时间戳
        return 时间对象.atZone(ZoneId.systemDefault()).toEpochSecond();
    }
    // 重载方法：简化参数（无增减）
    public static long to_time_unix(Object datetime_or_字符串or时间戳or时间对象) {
        return to_time_unix(datetime_or_字符串or时间戳or时间对象, 0, 0, 0, 0);
    }

    /**
     * 转换为时间元组（对应 Python: to_time_tuple，Java 用 long[] 模拟，顺序：年、月、日、时、分、秒、星期、年内天数、是否夏令时）
     * @param datetime_or_字符串or时间戳or时间对象 输入对象：String/Long/LocalDateTime/0
     * @param 增加几秒 增加秒数
     * @param 增加几分钟 增加分钟数
     * @param 增加几小时 增加小时数
     * @param 增加几天 增加天数
     * @return 时间元组数组
     */
    public static long[] to_time_tuple(
            Object datetime_or_字符串or时间戳or时间对象,
            long 增加几秒,
            long 增加几分钟,
            long 增加几小时,
            long 增加几天
    ) {
        LocalDateTime 时间对象 = to_time_datetime(datetime_or_字符串or时间戳or时间对象, 时间字符串_模板, 增加几秒, 增加几分钟, 增加几小时, 增加几天);
        // 模拟 Python time.struct_time 结构：(年,月,日,时,分,秒,星期,年内天数,是否夏令时)
        return new long[]{
                时间对象.getYear(),                // 年
                时间对象.getMonthValue(),          // 月
                时间对象.getDayOfMonth(),          // 日
                时间对象.getHour(),                // 时
                时间对象.getMinute(),              // 分
                时间对象.getSecond(),              // 秒
                时间对象.getDayOfWeek().getValue(),// 星期（1=周一，7=周日）
                时间对象.getDayOfYear(),           // 年内天数
                0                              // 是否夏令时（Java 不处理，默认0）
        };
    }


    /**
     * 获取当前 LocalDateTime（对应 Python: to_now_datetime）
     * @return 当前时间
     */
    public static LocalDateTime to_now_datetime() {
        return LocalDateTime.now();
    }
    public static String to_now_str(){
        return to_now_str("yyyy-MM-dd HH:mm:ss", false);
    }
    public static String to_now_str(String format){
        boolean 是否由oracle格式转为java格式 = is_oracle_format(format);
        return to_now_str(format, 是否由oracle格式转为java格式);
    }
    public static String to_now_str(String format, boolean 是否由oracle格式转为java格式){
        String finalFormat = format;
        if (是否由oracle格式转为java格式) {
            finalFormat = from_oracle_time_format_to_java_time_format(finalFormat);
        }

        LocalDateTime now = LocalDateTime.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern(finalFormat);
        String formattedDateTime = now.format(formatter);
        return formattedDateTime;
    }
    //#endregion

    //#region md5 + uuid
    public static String to_md5(String str) {
        try{
            // 创建 MessageDigest 实例，指定 MD5 算法
            MessageDigest md = MessageDigest.getInstance("MD5");

            // 添加要计算摘要的字节
            md.update(str.getBytes());

            // 完成哈希计算
            byte[] digest = md.digest();

            // 将字节数组转换为十六进制字符串
            StringBuilder hexString = new StringBuilder();
            for (byte b : digest) {
                hexString.append(String.format("%02x", b));
            }
            return hexString.toString();
        }
        catch (NoSuchAlgorithmException e){
            return "";
        }
    }

    public static String to_uuid(){
        return to_uuid(true);
    }
    public static String to_uuid(boolean 去除中横线) {
        UUID uuid = UUID.randomUUID();
        if (去除中横线) {
            return uuid.toString().replace("-", "");
        } else {
            return uuid.toString();
        }
    }
    public static String to_uuid2() {
        return to_uuid2("id");
    }
    public static String to_uuid2(String type) {
        return to_uuid2(type, "_");
    }
    public static String to_uuid2(String type, String 间隔符) {
        return type + 间隔符 + to_now_str("yyyyMMddHHmmss") + 间隔符 + to_uuid(true);
    }

    //#endregion

    //#endregion ======to_xxx======

    //#region ------is_xxx------
    /**
     * 判断字符串是否是数字（支持整数、小数、负数）
     * @param str 待判断的字符串
     * @return true 表示是数字，false 表示不是
     */
    public static boolean is_number(String str) {
        if (str == null || str.trim().isEmpty()) {
            return false;
        }
        // 使用正则匹配数字
        // ^-?\\d+$ 匹配整数
        // ^-?\\d+\\.\\d+$ 匹配小数
        return str.matches("-?\\d+(\\.\\d+)?");
    }
    //#endregion ======is_xxx======
}
