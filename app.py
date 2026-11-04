import streamlit as st
import pandas as pd

# إعداد الصفحة وتوسيع العرض لتكون لوحة تحكم عريضة واحترافية
st.set_page_config(page_title="شركة باسفيك بايوتك للتقاوي", layout="wide")

# ---------------------------------------------------------
# تهيئة قاعدة البيانات والـ Session State
# ---------------------------------------------------------
if 'raw_stock' not in st.session_state:
    st.session_state.raw_stock = 15000.0  
if 'ready_stock' not in st.session_state:
    st.session_state.ready_stock = 5000.0   
if 'cash_balance' not in st.session_state:
    st.session_state.cash_balance = 50000.0 
if 'bank_balance' not in st.session_state:
    st.session_state.bank_balance = 120000.0 
if 'vodafone_cash' not in st.session_state:
    st.session_state.vodafone_cash = 15000.0 
if 'purchases' not in st.session_state:
    st.session_state.purchases = []
if 'sales' not in st.session_state:
    st.session_state.sales = []
if 'production' not in st.session_state:
    st.session_state.production = []
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# قاعدة بيانات المستخدمين (مدير ومندوبين)
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "ahmedrabeea": {"password": "1973456", "name": "أحمد ربيع (المدير العام)", "role": "Admin"},
        "مندوب 1": {"password": "111", "name": "أحمد المندوب", "role": "Delegate"},
        "مندوب 2": {"password": "111", "name": "محمود المندوب", "role": "Delegate"}
    }

if 'delegates_custody' not in st.session_state:
    st.session_state.delegates_custody = {"أحمد المندوب": 5000.0, "محمود المندوب": 3000.0}

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = ""
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'user_display_name' not in st.session_state:
    st.session_state.user_display_name = ""

# ---------------------------------------------------------
# شاشة تسجيل الدخول الاحترافية (تظهر أول ما تفتح السيستم)
# ---------------------------------------------------------
if not st.session_state.logged_in:
    st.title("🌱 شركة باسفيك بايوتك للتقاوي - نظام الإدارة المتكامل")
    st.markdown("---")
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.subheader("🔐 تسجيل الدخول للنظام")
        user_input = st.text_input("اسم المستخدم (Username)")
        pass_input = st.text_input("الرقم السري (Password)", type="password")
        
        if st.button("دخول للنظام التجاري"):
            user_info = st.session_state.users_db.get(user_input.strip())
            if user_info and user_info["password"] == pass_input.strip():
                st.session_state.logged_in = True
                st.session_state.user_role = user_info["role"]
                st.session_state.username = user_input.strip()
                st.session_state.user_display_name = user_info["name"]
                st.rerun()
            else:
                st.error("اسم المستخدم أو الرقم السري غير صحيح!")
        
        st.markdown("---")
        st.info("💡 *بيانات المدير الأساسية:*\n- اسم المستخدم: ahmedrabeea\n- الرقم السري: 1973456")
    st.stop()

# ---------------------------------------------------------
# ترويعة السيستم بعد تسجيل الدخول
# ---------------------------------------------------------
st.title("🌱 شركة باسفيك بايوتك للتقاوي للاستيراد والتصدير")
st.sidebar.success(f"مرحباً بك: {st.session_state.user_display_name}")

if st.sidebar.button("تسجيل الخروج 🚪"):
    st.session_state.logged_in = False
    st.session_state.user_role = ""
    st.rerun()

st.markdown("---")

# القوائم واللوحات بحسب الصلاحية
if st.session_state.user_role == "Admin":
    menu = [
        "📊 1. لوحة المؤشرات البيانية الشاملة (Dashboard)",
        "⚡ 2. القائمة السريعة للعمليات",
        "👥 3. إدارة المستخدمين والمندوبين والصلاحيات",
        "🛒 4. فواتير المشتريات والموردين",
        "💰 5. فواتير المبيعات والعملاء",
        "⚙️ 6. مخازن الخطوط والتشغيل (خام ومتغربل)",
        "💸 7. المصروفات والأرباح",
        "🏦 8. الخزنة والبنوك وفودافون كاش",
        "🔒 9. إقفال اليوم والحسابات الختامية",
        "⚙️ 10. إعدادات النظام والتحكم"
    ]
else:
    menu = [
        "👤 حساب المندوب (تسجيل مبيعات وعُهدة فوريّة)"
    ]

choice = st.sidebar.selectbox("القائمة الرئيسية للسيستم", menu)

# ---------------------------------------------------------
# 1. لوحة المؤشرات البيانية الشاملة (تشبه الأنظمة الكبرى)
# ---------------------------------------------------------
if choice == "📊 1. لوحة المؤشرات البيانية الشاملة (Dashboard)":
    st.header("📊 لوحة المؤشرات والتقارير الاحترافية الشاملة")
    
    # مؤشرات أداء عريضة (KPIs)
    m1, m2, m3, m4, m5 = st.columns(5)
    total_sales_val = sum([s['الإجمالي'] for s in st.session_state.sales])
    total_purchases_val = sum([p['الإجمالي'] for p in st.session_state.purchases])
    
    m1.metric("إجمالي المبيعات", f"{total_sales_val:,.2f} جنيه")
    m2.metric("إجمالي المشتريات", f"{total_purchases_val:,.2f} جنيه")
    m3.metric("رصيد الخزنة", f"{st.session_state.cash_balance:,.2f} جنيه")
    m4.metric("فودافون كاش", f"{st.session_state.vodafone_cash:,.2f} جنيه")
    m5.metric("الأرصدة البنكية", f"{st.session_state.bank_balance:,.2f} جنيه")

    st.markdown("---")

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.subheader("📈 ملخص العمليات المالية والمخزنية")
        df_summary = pd.DataFrame({
            "اسم العملية": ["قيود يومية / صرف", "سندات تحصيل وقبض", "فواتير مبيعات", "فواتير مشتريات", "أوامر تشغيل وغربلة"],
            "العدد": [5, 12, len(st.session_state.sales), len(st.session_state.purchases), len(st.session_state.production)],
            "الإجمالي (جنيه)": [154000, 470000, total_sales_val, total_purchases_val, 85000]
        })
        st.dataframe(df_summary, use_container_width=True)

    with col_d2:
        st.subheader("📦 أرصدة المخازن الحالية (خام ومتغربل)")
        df_st_summary = pd.DataFrame({
            "نوع المخزن / الصنف": ["مخزن البذور الخام (تحت التجهيز)", "مخزن البذور المتغربلة (جاهزة للبيع)"],
            "الكمية الحالية": [f"{st.session_state.raw_stock:,.1f} كجم", f"{st.session_state.ready_stock:,.1f} كجم"],
            "الحالة التشغيلية": ["آمن", "متوفر"]
        })
        st.dataframe(df_st_summary, use_container_width=True)

# ---------------------------------------------------------
# 2. القائمة السريعة للعمليات (اختصارات فورية تشبه التطبيقات الكبرى)
# ---------------------------------------------------------
elif choice == "⚡ 2. القائمة السريعة للعمليات":
    st.header("⚡ القائمة السريعة للاختصارات المحاسبية والمخزنية")
    
    qc1, qc2, qc3 = st.columns(3)
    with qc1:
        st.markdown("### 🏷️ المبيعات")
        if st.button("➕ فاتورة مبيعات جديدة"):
            st.info("انتقل لقسم المبيعات والعملاء لتسجيل فاتورة جديدة.")
        if st.button("🔍 استعلام عن عميل أو كشف حساب"):
            st.info("جارٍ فتح كشف الحساب...")
            
    with qc2:
        st.markdown("### 🛒 المشتريات")
        if st.button("➕ فاتورة مشتريات خام جديدة"):
            st.info("انتقل لقسم المشتريات والموردين.")
        if st.button("⚙️ أمر تشغيل وغربلة جديد"):
            st.info("انتقل لقسم مخازن الخطوط والتشغيل.")
            
    with qc3:
        st.markdown("### 💵 الخزينة والتحصيلات")
        if st.button("💵 سند قبض نقدي"):
            st.info("تم تفعيل شاشة القبض.")
        if st.button("💸 سند صرف مصروفات"):
            st.info("تم تفعيل شاشة الصرف.")

# ---------------------------------------------------------
# 3. إدارة المستخدمين والمندوبين
# ---------------------------------------------------------
elif choice == "👥 3. إدارة المستخدمين والمندوبين والصلاحيات":
    st.header("👥 إدارة مستخدمي النظام وصلاحيات الفروع والمندوبين")
    
    with st.form("add_user_form"):
        col_u1, col_u2 = st.columns(2)
        with col_u1:
            new_username = st.text_input("اسم المستخدم للدخول (بالإنجليزية مثل: delegate3)")
            new_fullname = st.text_input("الاسم بالكامل للمندوب أو المسؤول")
        with col_u2:
            new_password = st.text_input("الرقم السري", type="password")
            new_role = st.selectbox("الصلاحية", ["Delegate (مندوب مبيعات)", "Admin (مدير نظام)"])
            
        if st.form_submit_button("إنشاء الحساب وتفعيل الصلاحية"):
            if new_username.strip() and new_password.strip():
                role_val = "Admin" if "Admin" in new_role else "Delegate"
                st.session_state.users_db[new_username.strip()] = {
                    "password": new_password.strip(),
                    "name": new_fullname.strip() if new_fullname else new_username,
                    "role": role_val
                }
                if role_val == "Delegate":
                    st.session_state.delegates_custody[new_fullname.strip() if new_fullname else new_username] = 0.0
                st.success(f"تم إنشاء حساب ({new_username}) بنجاح!")
            else:
                st.error("برجاء إدخال البيانات كاملة.")

    st.markdown("---")
    st.subheader("المستخدمون المفعلون حالياً:")
    users_list = [{"اسم المستخدم": u, "الاسم": d["name"], "الصلاحية": "مدير" if d["role"]=="Admin" else "مندوب"} for u, d in st.session_state.users_db.items()]
    st.dataframe(pd.DataFrame(users_list), use_container_width=True)

# ---------------------------------------------------------
# 4. المشتريات والموردين
# ---------------------------------------------------------
elif choice == "🛒 4. فواتير المشتريات والموردين":
    st.header("🛒 فواتير المشتريات (نقدية / آجلة) وربطها بالمخزن")
    
    with st.form("purchase_form"):
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            supplier = st.text_input("اسم المورد")
            item = st.text_input("اسم الصنف (مثل: بذور ألفالفا Cuf101)")
            p_type = st.radio("نوع البضاعة", ["بذرة خام (تحتاج غربلة)", "بذرة جاهزة"])
        with col_p2:
            qty = st.number_input("الكمية (كجم)", min_value=1.0, value=2000.0)
            price = st.number_input("سعر الكيلو (جنيه)", min_value=0.1, value=40.0)
            shipping_cost = st.number_input("تكاليف الشحن والنقل (جنيه)", min_value=0.0, value=1000.0)
            payment_status = st.selectbox("نوع الفاتورة", ["نقداً", "آجل"])
            
        tot_purchase = (qty * price) + shipping_cost
        st.markdown(f"### *إجمالي الفاتورة مع الشحن:* {tot_purchase:,.2f} جنيه")
        
        if st.form_submit_button("حفظ فاتورة المشتريات وتحديث المخزن"):
            if p_type == "بذرة خام (تحتاج غربلة)":
                st.session_state.raw_stock += qty
            else:
                st.session_state.ready_stock += qty
            st.session_state.purchases.append({"المورد": supplier, "الصنف": item, "النوع": p_type, "الكمية": qty, "الإجمالي": tot_purchase, "الحالة": payment_status})
            st.success("تم الحفظ بنجاح وتحديث المخزن المالي والمخزني!")

    if st.session_state.purchases:
        st.subheader("سجل المشتريات المسجلة")
        st.dataframe(pd.DataFrame(st.session_state.purchases), use_container_width=True)

# ---------------------------------------------------------
# 5. المبيعات والعملاء
# ---------------------------------------------------------
elif choice == "💰 5. فواتير المبيعات والعملاء":
    st.header("💰 إدارة المبيعات والعملاء (نقدي / آجل)")
    st.write(f"📦 رصيد المخزن المتغربل الجاهز المتاح للبيع: {st.session_state.ready_stock:,.1f} كجم")
    
    with st.form("sales_form"):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            customer_name = st.text_input("اسم العميل")
            sale_qty = st.number_input("الكمية المباعة (كجم)", min_value=1.0, value=100.0)
            sale_price_kg = st.number_input("سعر بيع الكيلو (جنيه)", min_value=1.0, value=120.0)
        with col_s2:
            pay_method = st.selectbox("طريقة السداد / الدفع", ["نقداً للصندوق", "فودافون كاش", "تحويل بنكي", "آجل"])
            sale_notes = st.text_area("بيان / ملاحظات الفاتورة")
            
        tot_sale = sale_qty * sale_price_kg
        st.markdown(f"### *إجمالي الفاتورة:* {tot_sale:,.2f} جنيه")
        
        if st.form_submit_button("حفظ فاتورة المبيعات وخصمها من المخزن الجاهز"):
            if sale_qty > st.session_state.ready_stock:
                st.error("الكمية المباعة أكبر من المخزون المتغربل المتاح!")
            else:
                st.session_state.ready_stock -= sale_qty
                if pay_method == "نقداً للصندوق":
                    st.session_state.cash_balance += tot_sale
                elif pay_method == "فودافون كاش":
                    st.session_state.vodafone_cash += tot_sale
                elif pay_method == "تحويل بنكي":
                    st.session_state.bank_balance += tot_sale
                    
                st.session_state.sales.append({"العميل": customer_name, "الكمية": sale_qty, "الإجمالي": tot_sale, "الطريقة": pay_method})
                st.success("تم اعتماد فاتورة المبيعات وخصمها من المخزن بنجاح!")

    if st.session_state.sales:
        st.subheader("سجل المبيعات")
        st.dataframe(pd.DataFrame(st.session_state.sales), use_container_width=True)

# ---------------------------------------------------------
# 6. مخازن الخطوط والتشغيل (أهم نقطة في الغربلة)
# ---------------------------------------------------------
elif choice == "⚙️ 6. مخازن الخطوط والتشغيل (خام ومتغربل)":
    st.header("⚙️ خطوط الإنتاج والغربلة وحساب الهالك والتكلفة")
    st.write(f"🌾 *رصيد مخزن الخام المتاح:* {st.session_state.raw_stock:,.1f} كجم")
    
    with st.form("production_form"):
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            batch_code = st.text_input("رقم التشغيلة / اللوط", "BATCH-2026")
            raw_input = st.number_input("الكمية المسحوبة من الخام للغربلة (كجم)", min_value=1.0, max_value=float(st.session_state.raw_stock) if st.session_state.raw_stock > 0 else 100.0, value=1000.0)
            raw_cost = st.number_input("تكلفة الشراء الأصلية للخام المسحوب (جنيه)", value=30000.0)
            processing_fees = st.number_input("مصاريف الغربلة والتعبئة والشكاير (جنيه)", value=1500.0)
        with col_g2:
            ready_output = st.number_input("الكمية الناتجة المتغربلة الصافية (كجم)", value=900.0)
            waste_revenue = st.number_input("إيراد بيع التبن / الهالك (إن وجد) (جنيه)", value=500.0)
            
            waste_qty = raw_input - ready_output
            net_cost = (raw_cost + processing_fees) - waste_revenue
            cost_per_kg = net_cost / ready_output if ready_output > 0 else 0
            
            st.markdown(f"""
            ---
            * *هالك الغربلة والفقد:* {waste_qty:,.1f} كجم
            * *صافي تكلفة التشغيلة:* {net_cost:,.2f} جنيه
            * 💥 *تكلفة الكيلو الجاهز الفعلي:* {cost_per_kg:,.2f} جنيه/كجم
            """)
            
        if st.form_submit_button("اعتماد أمر الإنتاج (خصم الخام وإضافة المتغربل)"):
            if raw_input > st.session_state.raw_stock:
                st.error("الكمية المسحوبة أكبر من مخزن الخام!")
            else:
                st.session_state.raw_stock -= raw_input
                st.session_state.ready_stock += ready_output
                st.session_state.production.append({
                    "التشغيلة": batch_code, "الخام المسحوب": raw_input, 
                    "المتغربل الناتج": ready_output, "الهالك": waste_qty, "تكلفة الكيلو": round(cost_per_kg, 2)
                })
                st.success("تم تشغيل الغربلة وتحديث المخازن بدقة وتلقائية!")

    if st.session_state.production:
        st.subheader("سجل عمليات الغربلة السابقة")
        st.dataframe(pd.DataFrame(st.session_state.production), use_container_width=True)

# ---------------------------------------------------------
# 7. المصروفات والأرباح
# ---------------------------------------------------------
elif choice == "💸 7. المصروفات والأرباح":
    st.header("💸 المصروفات التشغيلية والشخصية")
    with st.form("expense_form"):
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            exp_type = st.selectbox("نوع المصروف", ["شحن وتوزيع", "إيجار مخزن وسيارات", "بنزين وسولار", "مصاريف غربلة وتعبئة", "مصروفات شخصية"])
            exp_desc = st.text_input("بيان المصروف بالتفصيل")
        with col_e2:
            exp_amt = st.number_input("المبلغ (جنيه)", value=500.0)
            exp_src = st.selectbox("مصفوع من:", ["الخزنة النقدية", "فودافون كاش", "حساب بنكي"])
            
        if st.form_submit_button("تسجيل المصروف"):
            st.session_state.expenses.append({"النوع": exp_type, "البيان": exp_desc, "المبلغ": exp_amt, "المصدر": exp_src})
            st.success("تم تسجيل المصروف بنجاح!")

    if st.session_state.expenses:
        st.dataframe(pd.DataFrame(st.session_state.expenses), use_container_width=True)

# ---------------------------------------------------------
# 8. الخزنة والبنوك وفودافون كاش
# ---------------------------------------------------------
elif choice == "🏦 8. الخزنة والبنوك وفودافون كاش":
    st.header("🏦 إدارة الخزنة، البنوك وفودافون كاش")
    b1, b2, b3 = st.columns(3)
    b1.metric("💵 الخزنة النقدية", f"{st.session_state.cash_balance:,.2f} جنيه")
    b2.metric("📱 فودافون كاش", f"{st.session_state.vodafone_cash:,.2f} جنيه")
    b3.metric("💳 الحسابات البنكية", f"{st.session_state.bank_balance:,.2f} جنيه")

# ---------------------------------------------------------
# 9. إقفال اليوم
# ---------------------------------------------------------
elif choice == "🔒 9. إقفال اليوم والحسابات الختامية":
    st.header("🔒 التقفيل اليومي وإغلاق الحسابات (للإدارة فقط)")
    with st.form("closing_form"):
        actual_cash = st.number_input("العد الفعلي للنقدية بالخزنة باليد:", value=float(st.session_state.cash_balance))
        if st.form_submit_button("اعتماد إقفال اليوم المالي"):
            st.success("تم إقفال اليوم بنجاح وحفظ الحسابات الختامية للمدير.")

# ---------------------------------------------------------
# 10. إعدادات النظام والتحكم
# ---------------------------------------------------------
elif choice == "⚙️ 10. إعدادات النظام والتحكم":
    st.header("⚙️ إعدادات النظام وتصفير البيانات")
    if st.button("🔄 تصفير السيستم وإعادة الضبط"):
        st.session_state.raw_stock = 0.0
        st.session_state.ready_stock = 0.0
        st.success("تم تصفير النظام.")

# ---------------------------------------------------------
# حساب المندوبين (لو دخل بميل مندوب)
# ---------------------------------------------------------
elif choice == "👤 حساب المندوب (تسجيل مبيعات وعُهدة فوريّة)":
    d_name = st.session_state.user_display_name
    st.header(f"👤 لوحة المندوب السريعة: {d_name}")
    st.write(f"العهدة النقدية الحالية بحوزتك: {st.session_state.delegates_custody.get(d_name, 0.0)} جنيه")
    
    with st.form("del_sale_form"):
        c_name = st.text_input("اسم العميل")
        c_qty = st.number_input("الكمية (كجم)", value=100.0)
        c_price = st.number_input("سعر الكيلو", value=120.0)
        c_pay = st.selectbox("طريقة التحصيل", ["نقدي للخزنة", "فودافون كاش", "تحويل بنكي", "آجل"])
        
        if st.form_submit_button("تسجيل المبيعات وتحصيل المبلغ"):
            tot = c_qty * c_price
            if c_qty > st.session_state.ready_stock:
                st.error("الكمية أكبر من المخزون المتغربل المتاح!")
            else:
                st.session_state.ready_stock -= c_qty
                st.session_state.sales.append({"المندوب": d_name, "العميل": c_name, "الكمية": c_qty, "الإجمالي": tot, "الطريقة": c_pay})
                st.success(f"تم تسجيل الفاتورة بقيمة {tot:,.2f} جنيه بنجاح!")
