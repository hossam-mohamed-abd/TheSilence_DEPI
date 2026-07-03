import requests
from bs4 import BeautifulSoup
import pandas as pd

# رابط الصفحة
url = "https://ar.wikipedia.org/wiki/%D9%82%D8%A7%D8%A6%D9%85%D8%A9_%D9%85%D8%AF%D9%86_%D9%85%D8%B5%D8%B1"

# إرسال طلب لجلب محتوى الصفحة
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
response = requests.get(url, headers=headers)
response.encoding = 'utf-8' # للتأكد من قراءة اللغة العربية بشكل صحيح

# قائمة لتخزين البيانات المستخرجة
all_cities_data = []

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # البحث عن كل العناوين الرئيسية للمحافظات (والتي تأتي غالباً كـ h3 أو h4 في ويكيبيديا بجانبها جداول)
    # أو يمكننا البحث مباشرة عن الجداول التي تحتوي على المدن
    
    # سنجد كل الجداول من نوع 'wikitable' التي تحتوي على قائمة المدن
    tables = soup.find_all('table', class_='wikitable')
    
    for table in tables:
        # لمحاولة معرفة اسم المحافظة، نبحث عن العنوان السابث للجدول مباشرة
        prev_element = table.find_previous(['h3', 'h4', 'h2'])
        governorate_name = prev_element.text.replace('[عدل]', '').strip() if prev_element else "غير معروف"
        
        # تخطي الجداول العامة التي لا تمثل محافظات محددة إذا وجدت
        if "مدن" not in governorate_name and "محافظة" not in governorate_name:
            continue
            
        # المرور على صفوف الجدول (باستثناء صف العنوان الأول)
        rows = table.find_all('tr')[1:]
        for row in rows:
            cols = row.find_all(['td', 'th'])
            
            # للتأكد من أن الصف يحتوي على بيانات وليس صفاً فارغاً
            if len(cols) >= 3:
                # في جداول ويكيبيديا هذه، اسم المدينة غالباً يكون في العمود الثاني أو الثالث 
                # سنقوم بالبحث عن أول رابط نصي (أو نص) داخل الأعمدة يمثل اسم المدينة
                city_name = ""
                
                # نبحث في الأعمدة لمعرفة عمود "المدينة" (غالباً العمود المكتوب فيه اسم المدينة مباشرة)
                # بناءً على بنية الجدول: العمود 0: الرقم، العمود 1: المدينة أو الصورة
                for col in cols:
                    # إذا كان العمود يحتوي على رابط وتشير النصوص لاسم مدينة
                    a_tag = col.find('a')
                    if a_tag and a_tag.text.strip():
                        # نتأكد من أنه ليس رقماً أو سنة
                        if not a_tag.text.strip().isdigit():
                            city_name = a_tag.text.strip()
                            break
                
                if not city_name:
                    # محاولة بديلة إذا لم يكن هناك رابط
                    city_name = cols[1].text.strip()
                
                # تنظيف النص المستخرج
                city_name = city_name.split('\n')[0].strip()
                
                # إضافة البيانات للقائمة
                if city_name and not city_name.isdigit() and len(city_name) > 2:
                    all_cities_data.append({
                        'المحافظة': governorate_name,
                        'المدينة': city_name
                    })

    # تحويل البيانات إلى DataFrame لتنسيقها وحفظها
    df = pd.DataFrame(all_cities_data)
    
    # تنظيف أسماء المحافظات (إزالة كلمة "مدن محافظة" لتبسيط الاسم)
    df['المحافظة'] = df['المحافظة'].str.replace('مدن ', '', regex=False)
    
    # حذف التكرارات إن وجدت
    df.drop_duplicates(inplace=True)
    
    # عرض أول 20 نتيجة للتأكد
    print(df.head(249))
    
    # حفظ النتائج في ملف Excel أو CSV
    df.to_csv('egypt_cities.csv', index=False, encoding='utf-8-sig')
    print(f"\nتم استخراج {len(df)} مدينة بنجاح وحفظها في ملف 'egypt_cities.csv'")

else:
    print(f"فشل الاتصال بالموقع. رمز الخطأ: {response.status_code}")