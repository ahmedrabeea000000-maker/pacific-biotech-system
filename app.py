import streamlit as st
import pandas as pd

# إعداد الصفحة وتوسيع العرض
st.set_page_config(page_title="شركة باسفيك بايوتك للتقاوي", layout="wide")

# ---------------------------------------------------------
# تهيئة قاعدة البيانات المؤقتة في الـ Session State
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
if 'delegates_custody' not in st.session_state:
    st.session_state.delegates_custody = {"أحمد المندوب": 5000.0, "محمود المندوب": 3000.0}

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = ""
if 'username' not in st.session_state:
    st.session_state.username = ""

# ---------------------------------------------------------
# شاشة تسجيل الدخول الآمنة
# ---------------------------------------------------------
if not st.session_state.logged_in:
    st.title("🌱 نظام شركة باسفيك بايوتك للتقاوي - تسجيل الدخول")
    st.markdown("---")
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.subheader("تسجيل الدخول للنظام")
        role_choice = st.selectbox("اختر نوع المستخدم", ["مدير النظام (الإدارة العليا)", "مندوب مبيعات"])
        
        if role_choice == "مدير النظام (الإدارة العليا)":
            pass_input = st.text_input("كلمة مرور المدير", type="password")
            if st.button("دخول المدير"):
                if pass_input == "1234":  # كلمة مرور المدير الافتراضية ويمكن تغييرها
                    st.session_state.logged_in = True
                    st.session_state.user_role = "Admin"
                    st.session_state.username = "المدير العام"
                    st.rerun()
                else:
                    st.error("كلمة المرور غير صحيحة!")
        else:
            del_name = st.selectbox("اختر اسم المندوب", ["أحمد المندوب", "محمود المندوب"])
            del_pass = st.text_input("كلمة مرور المندوب", type="password")
            if st.button("دخول المندوب"):
                if del_pass == "111":  # كلمة مرور المندوبين
                    st.session_state.logged_in = True
                    st.session_state.user_role = "Delegate"
                    st.session_state.username = del_name
                    st.rerun()
                else:
                    st.error("كلمة المرور غير صحيحة!")
    st.stop()

# ---------------------------------------------------------
# لوحة التحكم بعد تسجيل الدخول (بناءً على الصلاحيات)
# ---------------------------------------------------------
st.title("🌱 شركة باسفيك بايوتك للتقاوي للاستيراد والتصدير")
st.sidebar.success(f"مرحباً بك: {st.session_state.username} ({'المدير' if st.session_state.user_role == 'Admin' else 'مندوب'})")

if st.sidebar.button("تسجيل الخروج 🚪"):
    st.session_state.logged_in = False
    st.session_state.user_role = ""
    st.rerun()

st.markdown("---")

# تحديد القوائم بناءً على صلاحية المستخدم
if st.session_state.user_role == "Admin":
    menu = [
        "🏠 1. الصفحة الرئيسية واللوحة العامة",
        "👑 2. حساب المدير والرقابة",
        "🛒 4. المشتريات والموردين",
        "💰 5. المبيعات والعملاء",
        "⚙️ 6. المخازن والتشغيل (خام ومتغربل)",
        "💸 7. المصروفات والأرباح",
        "🏦 8. الخزنة والبنوك وفودافون كاش",
        "🔒 9. إقفال اليوم والحسابات الختامية",
        "📊 10. التقارير والطباعة الشاملة",
        "⚙️ 11. إعدادات النظام والتحكم"
    ]
else:
    # المندوب يشاهد صفحته وحساباته الخاصة فقط دون الوصول للإدارة أو المشتريات
    menu = [
        "👤 3. حساب المندوبين (تسجيل مبيعات وعُهدة)"
    ]

choice = st.sidebar.selectbox("اختر القسم", menu)

# ---------------------------------------------------------
# 1. الصفحة الرئيسية واللوحة العامة (مدير فقط)
# ---------------------------------------------------------
if choice == "🏠 1. الصفحة الرئيسية واللوحة العامة":
    st.header("🏠 لوحة المؤشرات العامة للشركة")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("إجمالي المبيعات", f"{sum([s['الإجمالي'] for s in st.session_state.sales]):,.2f} جنيه")
    m2.metric("إجمالي المشتريات", f"{sum([p['الإجمالي'] for p in st.session_state.purchases]):,.2f} جنيه")
    m3.metric("رصيد الخزنة النقدية", f"{st.session_state.cash_balance:,.2f} جنيه")
    m4.metric("رصيد فودافون كاش", f"{st.session_state.vodafone_cash:,.2f} جنيه")
    m5.metric("رصيد البنوك", f"{st.session_state.bank_balance:,.2f} جنيه")

    st.markdown("---")
    col_st1, col_st2 = st.columns(2)
    with col_st1:
        st.subheader("📦 المخزون المتاح حالياً")
        st.info(f"🌾 *مخزن بذور خام:* {st.session_state.raw_stock:,.1f} كجم")
        st.success(f"✨ *مخزن بذور متغربلة وجاهزة:* {st.session_state.ready_stock:,.1f} كجم")
    with col_st2:
        st.subheader("🔔 التنبيهات وحالة السيستم")
        st.success("✅ النظام آمن ويعمل بصلاحيات المدير الكاملة.")

# ---------------------------------------------------------
# 2. حساب المدير والرقابة
# ---------------------------------------------------------
elif choice == "👑 2. حساب المدير والرقابة":
    st.header("👑 لوحة تحكم المدير العام والرقابة الشاملة")
    custody_df = pd.DataFrame(list(st.session_state.delegates_custody.items()), columns=["اسم المندوب", "العهدة النقدية الحالية (جنيه)"])
    st.dataframe(custody_df, use_container_width=True)

# ---------------------------------------------------------
# 3. حساب المندوب (خاص بالمندوبين)
# ---------------------------------------------------------
elif choice == "👤 3. حساب المندوبين (تسجيل مبيعات وعُهدة)":
    delegate_name = st.session_state.username
    st.header(f"👤 لوحة المندوب: {delegate_name}")
    st.write(f"العهدة النقدية الحالية بحوزتك: {st.session_state.delegates_custody.get(delegate_name, 0)} جنيه")
    
    with st.form("delegate_action_form"):
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            cust_name = st.text_input("اسم العميل")
            seed_qty = st.number_input("الكمية المباعة (كجم)", min_value=1.0, value=100.0)
            sale_price = st.number_input("سعر البيع للكيلو (جنيه)", min_value=1.0, value=120.0)
        with col_d2:
            collection_type = st.selectbox("طريقة التحصيل", ["نقدي للخزنة", "فودافون كاش", "تحويل بنكي", "آجل"])
            notes = st.text_area("ملاحظات المندوب")
            
        submit_del_sale = st.form_submit_button("تسجيل عملية البيع وتحصيل المبلغ")
        if submit_del_sale:
            total_sale_amt = seed_qty * sale_price
            if seed_qty > st.session_state.ready_stock:
                st.error("الكمية المطلوبة أكبر من المخزون المتغربل الجاهز المتاح!")
            else:
                st.session_state.ready_stock -= seed_qty
                if collection_type == "نقدي للخزنة":
                    st.session_state.cash_balance += total_sale_amt
                elif collection_type == "فودافون كاش":
                    st.session_state.vodafone_cash += total_sale_amt
                elif collection_type == "تحويل بنكي":
                    st.session_state.bank_balance += total_sale_amt
                    
                st.session_state.sales.append({
                    "المندوب": delegate_name,
                    "العميل": cust_name,
                    "الكمية": seed_qty,
                    "الإجمالي": total_sale_amt,
                    "الطريقة": collection_type
                })
                st.success(f"تم تسجيل عملية البيع بنجاح بقيمة {total_sale_amt:,.2f} جنيه وخصمها من المخزن!")

# ---------------------------------------------------------
# 4. المشتريات والموردين
# ---------------------------------------------------------
elif choice == "🛒 4. المشتريات والموردين":
    st.header("🛒 إدارة المشتريات والموردين")
    with st.form("purchase_section_form"):
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            supplier = st.text_input("اسم المورد")
            item = st.text_input("اسم الصنف")
            p_type = st.radio("نوع البضاعة", ["بذرة خام (تحتاج غربلة)", "بذرة جاهزة"])
        with col_p2:
            qty = st.number_input("الكمية (كجم)", min_value=1.0, value=2000.0)
            price = st.number_input("سعر الكيلو (جنيه)", min_value=0.1, value=40.0)
            shipping_cost = st.number_input("تكاليف الشحن والنقل (جنيه)", min_value=0.0, value=1000.0)
            payment_status = st.selectbox("حالة السداد", ["نقدى بالكامل", "آجل"])
            
        tot_purchase = (qty * price) + shipping_cost
        save_purchase = st.form_submit_button("حفظ الفاتورة وتحديث المخزن")
        if save_purchase:
            if p_type == "بذرة خام (تحتاج غربلة)":
                st.session_state.raw_stock += qty
            else:
                st.session_state.ready_stock += qty
            st.session_state.purchases.append({"المورد": supplier, "الصنف": item, "النوع": p_type, "الكمية": qty, "الإجمالي": tot_purchase})
            st.success("تم حفظ الفاتورة وتحديث المخزن بنجاح!")

    if st.session_state.purchases:
        st.dataframe(pd.DataFrame(st.session_state.purchases), use_container_width=True)

# ---------------------------------------------------------
# 5. المبيعات والعملاء
# ---------------------------------------------------------
elif choice == "💰 5. المبيعات والعملاء":
    st.header("💰 إدارة المبيعات العامة للشركة")
    if st.session_state.sales:
        st.dataframe(pd.DataFrame(st.session_state.sales), use_container_width=True)
    else:
        st.info("لا توجد مبيعات مسجلة حتى الآن.")

# ---------------------------------------------------------
# 6. المخازن والتشغيل
# ---------------------------------------------------------
elif choice == "⚙️ 6. المخازن والتشغيل (خام ومتغربل)":
    st.header("⚙️ إدارة خطوط الإنتاج والغربلة")
    with st.form("production_line_form"):
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            batch_no = st.text_input("رقم التشغيلة", "BATCH-1")
            raw_withdrawn = st.number_input("الكمية المسحوبة من الخام (كجم)", min_value=1.0, max_value=float(st.session_state.raw_stock) if st.session_state.raw_stock > 0 else
