import os.path

JAVA_MESSAGE_DIR = "E:/CornerAndroid/app/src/main/java/com/astatus/cornerandroid/message/";
JS_MEESSAGE_DIR = "D:/CornerServer/message/";

LINE_TYPE_INVALID = 1;
LINE_TYPE_CLASS_BEGIN_DEFINE = 2;
LINE_TYPE_PARAM_DEFINE = 3;
LINE_TYPE_CLASS_END_DEFINE = 4;
LINE_TYPE_EMPTY_DEFINE = 5;
LINE_TYPE_ANNOTATOPN_DEFINE = 6;
LINE_TYPE_STATIC_FINAL_DEFINE = 7;
LINE_TYPE_ARRAY_PARAM_DEFINE = 8;

def check_line_type(subs):
    length = len(subs)
    if length == 4 and subs[3] == '{':
        return LINE_TYPE_CLASS_BEGIN_DEFINE;
    elif length == 3:
            if subs[1][0:9] == 'ArrayList':
                return LINE_TYPE_ARRAY_PARAM_DEFINE;
            else:
                return LINE_TYPE_PARAM_DEFINE;
    elif length == 1 and subs[0] == '}':
        return LINE_TYPE_CLASS_END_DEFINE;
    elif length == 0:
        return  LINE_TYPE_EMPTY_DEFINE;
    elif length == 1 and subs[0][0:2] == '//':
        return LINE_TYPE_ANNOTATOPN_DEFINE;
    elif length == 7:
        return LINE_TYPE_STATIC_FINAL_DEFINE;
    else:
        return LINE_TYPE_INVALID;

def convert_line(type, param0, param1, param3):
    content = ''
    if type == LINE_TYPE_CLASS_BEGIN_DEFINE:
        content = 'function ' + param0 + '(){';
    elif type == LINE_TYPE_PARAM_DEFINE:
        content = '    this.' + param0;
    elif type == LINE_TYPE_ARRAY_PARAM_DEFINE:
        content = '    this.' + param0[0:len(param0) - 1] + ' = new Array();';
    elif type == LINE_TYPE_CLASS_END_DEFINE:
        content = '}';
    elif type == LINE_TYPE_ANNOTATOPN_DEFINE:
        content = param0;
    elif type == LINE_TYPE_STATIC_FINAL_DEFINE:
        content = param0 + '.' + param1 + ' = ' + param3;
    return content + '\n';

def find_valid_lines(lines):
    valid_lines = [];
    is_valid_start = False;

    for line in lines:
        subs = line.split()
        length = len(subs)
        if not is_valid_start:
            if length == 4 and subs[0] == 'public' and subs[3] == '{':
                is_valid_start = True;
                valid_lines.append(line)
        else:
            valid_lines.append(line)

    return valid_lines;

def converter_file(file_name, lines):

    class_lines = [];
    final_lines = [];
    for line in lines:
        subs = line.split()
        type = check_line_type(subs)
        if type == LINE_TYPE_CLASS_BEGIN_DEFINE:
            class_lines.append(convert_line(type, subs[2], 0, 0));
        elif type == LINE_TYPE_PARAM_DEFINE:
            class_lines.append(convert_line(type, subs[2], 0, 0));
        elif type == LINE_TYPE_ARRAY_PARAM_DEFINE:
            class_lines.append(convert_line(type, subs[2], 0, 0));
        elif type == LINE_TYPE_CLASS_END_DEFINE:
            class_lines.append(convert_line(type, subs[0], 0, 0));
        elif type == LINE_TYPE_STATIC_FINAL_DEFINE:
            final_lines.append(convert_line(type, file_name, subs[4], subs[6]));
        elif type == LINE_TYPE_EMPTY_DEFINE:
            class_lines.append('\n');
        elif type == LINE_TYPE_ANNOTATOPN_DEFINE:
            class_lines.append('    ' + subs[0] + '\n');
        else:
            raise Exception('new file name:' + file_name + ' line error:' + line);

    final_lines.append('\nmodule.exports = ' + file_name);

    js_file = open(JS_MEESSAGE_DIR + file_name + '.js', 'w');
    js_file.writelines(class_lines);
    js_file.writelines(final_lines);
    js_file.close();

def main():
    file_names = os.listdir(JAVA_MESSAGE_DIR)
    for file_name in file_names:
            print(file_name)
            names = os.path.splitext(file_name);
            if names[1] == '.java' and names[0] != 'MessagePacket':
                f = open(JAVA_MESSAGE_DIR + file_name)
                lines = f.readlines()
                new_file_name = names[0] ;

                valid_lines = find_valid_lines(lines)
                converter_file(new_file_name, valid_lines)

if __name__ == '__main__':
    main()