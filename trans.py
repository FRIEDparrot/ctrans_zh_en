import os
import re
import time
import warnings
import concurrent.futures
import translators as ts

open_encoding = 'gbk'
dst_encoding = 'utf-8'
max_retry_time = 3
translator = 'bing'
use_google_for_better_trans = True

def translate_comments(file_path):
    cnt = 0
    with open(file_path, 'r', encoding=open_encoding) as f:
        lines = f.readlines()
    with open(file_path, 'w', encoding=dst_encoding) as f:
        for line in lines:
            # Find comments in the line
            comments = re.findall(r'//.*|/\* .*|\* .*', line)   # also  '*' will be  captured  here
            # remove the comments without Chinese Character
            comments = ['' if not re.search(r'[\u4e00-\u9fff]+', comment) else comment for comment in comments]
            comments = list(filter(None, comments))

            l = len(comments)
            for i in range(l):
                comment = comments[i]
                if (re.match(r"^\s*//", comment)) or (re.match(r"^\s*/\*", comment)):   # starts with // or /*
                    # the whole line is considered as comment,
                    if (re.match(r"^\s*//", comment)):
                        comment = re.sub(r"^\s*//",'',comment)
                    elif re.match(r"^\s*/\*", comment):
                        comment = re.sub(r"^/\*", '', comment)
                    if re.search(r"\*/\s*$", comment):
                        comment = re.sub(r"\*/\s*$",'',comment)
                elif (re.search(r"\*.*;", comment)):    # * + program sentence + comment (optional)
                    sub_comments = re.findall(r"//.*|/\* .*", comment)
                    sub_comments = list(filter(None, sub_comments))
                    comment = ''   # delete this comment and add sub comment
                    for c in sub_comments:
                        if re.match(r"//", c) or re.match(r"/\*", c):
                            c = c[2:]
                        if re.search(r"\*/\s*$", c):
                            c = re.sub(r"\*/\s*$",'',c);
                        comments.append(c)
                elif re.match(r"^\s*\*",comment):      #  * + Chinese Sentences  + (*/) optional
                    if not re.search(r"\*.*;", comment):
                        comment = re.sub(r"^s?\*",'', comment) # remove * before comment
                        if re.search(r"\*/\s*$", comment):
                            comment = re.sub(r"\*/\s*$", '',comment)
                    # else retain the string and not process it to prevent destory code
                else:
                    warnings.warn("can't process comment: %s"%(comment))
                comments[i] = comment

            comments = list(filter(None, comments))
            for comment in comments:
                cnt = cnt + 1
                translated_comment = translate_sentence(comment)
                line = line.replace(comment, translated_comment);
            f.write(line)
    return cnt

def translate_sentence(comment:str):
    engine = translator
    # Translate the comment to English
    retry = 0
    while retry < max_retry_time:
        try:
            translated_comment = ts.translate_text(comment, translator=translator, from_language='zh',
                                                   to_language='en')
            break;
        except Exception as e:
            warnings.warn(f"Error: {e}. Retrying after 15 second.")
            time.sleep(15)
            retry = retry + 1
    if (retry == max_retry_time):
        raise Exception("Exceed retry times %d" % (max_retry_time))
    # if there is still Chinese in translated sentences, translate it with google
    if (re.search(r'[\u4e00-\u9fff]+', translated_comment) and use_google_for_better_trans):
        while retry < max_retry_time:
            try:
                translated_comment = ts.translate_text(comment, translator='google', from_language='auto',
                                                       to_language='en')
                engine = 'google'
                break;
            except Exception as e:
                warnings.warn(f"Error: {e}. Retrying after 25 second.")
                time.sleep(25)
                retry = retry + 1
    # Replace the original comment with the translated comment
    print("engine ", engine, ":", comment, " ----> ", translated_comment)  # comment this if output not used
    return translated_comment

def main():
    time1 = time.time()
    cnt_tot = 0
    # Walk through the working directory
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for root, dirs, files in os.walk("."):
            for file in files:
                # Check if the file is a .c or .h file
                if file.endswith('.c') or file.endswith('.h') or file.endswith('.cpp'):
                    print("tranlating:", file)
                    file_path = os.path.join(root, file)
                    futures.append(executor.submit(translate_comments, file_path))
        for future in concurrent.futures.as_completed(futures):
            cnt_tot += future.result()
    time2 = time.time()
    print("translate %d sentences, time used is %s s"%(cnt_tot,time2-time1))

if __name__ == "__main__":
    # ts.preaccelerate_and_speedtest()
    main()
