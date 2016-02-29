import os.path

JAVA_MESSAGE_DIR = "D:/CornerAndroid/app/src/main/java/com/astatus/cornerandroid/message/";
JS_MEESSAGE_DIR = "D:/CornerServer/message/";

LINE_TYPE_INVALID = 1;
LINE_TYPE_CLASS_BEGIN_DEFINE = 2;
LINE_TYPE_PARAM_DEFINE = 3;
LINE_TYPE_CLASS_END_DEFINE = 4;

def check_line_type(subs):
    length = len(subs)
    if length == 4 and subs[3] == '{':
        return LINE_TYPE_CLASS_BEGIN_DEFINE;
    elif length == 3:
        return LINE_TYPE_PARAM_DEFINE;
    elif length == 1 and subs[0] == '}':
        return LINE_TYPE_CLASS_END_DEFINE;
    else:
        return LINE_TYPE_INVALID;

def convert_line(type, param0):
    content = ''
    if type == LINE_TYPE_CLASS_BEGIN_DEFINE:
        content = 'function ' + param0 + '(){';
    elif type == LINE_TYPE_PARAM_DEFINE:
        content = '    this.' + param0;
    elif type == LINE_TYPE_CLASS_END_DEFINE:
        content = '}';

    return content + '\n';

def converter_file(file_name, lines):

    newlines = [];
    for line in lines:
        subs = line.split()
        type = check_line_type(subs)
        if type == LINE_TYPE_CLASS_BEGIN_DEFINE:
            newlines.append(convert_line(type, subs[2]))
        elif type == LINE_TYPE_PARAM_DEFINE:
            newlines.append(convert_line(type, subs[2]))
        elif type == LINE_TYPE_CLASS_END_DEFINE:
            newlines.append(convert_line(type, subs[0]))
        else:
            Exception("new file name:" + file_name + " line error:" + line);

        js_file = open(JS_MEESSAGE_DIR + file_name, 'w');
        js_file.writelines(newlines);
        js_file.close();

def main():
    file_names = os.listdir(JAVA_MESSAGE_DIR)
    for file_name in file_names:
            print(file_name)
            names = os.path.splitext(file_name);
            if names[1] == '.java':
                f = open(JAVA_MESSAGE_DIR + file_name)
                lines = f.readlines()
                new_file_name = names[0] + '.js';
                converter_file(new_file_name, lines)

if __name__ == '__main__':
    main()