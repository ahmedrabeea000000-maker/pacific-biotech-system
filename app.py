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

# قاعدة بيانات المستخدمين والمندوبين (يمكن إضافتهم من شاشة المدير)
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
# شاشة تسجيل الدخول الأساسية
# ---------------------------------------------------------
if not st.session_state.logged_in:
    st.title("🌱 شركة باسفيك بايوتك للتقاوي - تسجيل الدخول")
    st.markdown("---")
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.subheader("تسجيل الدخول للنظام التجاري")
        
        user_input = st.text_input("اسم المستخدم (Username)")
        pass_input = st.text_input("الرقم السري (Password)", type="password")
        
        if st.button("دخول للنظام"):
            user_info = st.session_state.users_db.get(user_input.strip())
            if user_info and user_info["password"] == pass_input.strip():
                st.session_state.logged_in = True
                st.session_state.user_role = user_info["role"]
                st.session_state.username = user_input.strip()
                st.session_state.user_display_name = user_info["name"]
                st.rerun()
            else:
                st.error("اسم المستخدم أو الرقم السري غير صحيح!")
        
        st.info("💡 بيانات المدير الافتراضية:\n- اسم المستخدم: `ahmedrabeea`\n- الرقم السري: `1973456`")
    st.stop()

# ---------------------------------------------------------
# بعد تسجيل الدخول بنجاح
# ---------------------------------------------------------
st.title("🌱 شركة باسفيك بايوتك للتقاوي للاستيراد والتصدير")
st.sidebar.success(f"مرحباً بك: {st.session_state.user_display_name}")

if st.sidebar.button("تسجيل الخروج 🚪"):
    st.session_state.logged_in = False
    st.session_state.user_role = ""
    st.rerun()

st.markdown("---")

# تحديد القوائم بناءً على الصلاحية (مدير أو مندوب)
if st.session_state.user_role == "Admin":
    menu = [
        "🏠 1. الصفحة الرئيسية واللوحة العامة",
        "👥 2. إدارة المستخدمين والصلاحيات (أنت المسؤول)",
        "🛒 3. المشتريات والموردين",
        "💰 4. المبيعات والعملاء",
        "⚙️ 5. المخازن والتشغيل (خام ومتغربل)",
        "💸 6. المصروفات والأرباح",
        "🏦 7. الخزنة والبنوك وفودافون كاش",
        "🔒 8. إقفال اليوم والحسابات الختامية",
        "📊 9. التقارير والطباعة الشاملة",
        "⚙️ 10. إعدادات النظام والتحكم"
    ]
else:
    menu = [
        "👤 حساب المندوب (تسجيل مبيعات وعُهدة)"
    ]

choice = st.sidebar.selectbox("اختر القسم", menu)

# ---------------------------------------------------------
# أقسام السيستم
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
        st.info(f"🌾 **مخزن بذور خام:** {st.session_state.raw_stock:,.1f} كجم")
        st.success(f"✨ **مخزن بذور متغربلة وجاهزة:** {st.session_state.ready_stock:,.1f} كجم")
    with col_st2:
        st.subheader("🔔 حالة السيستم")
        st.success("✅ أهلاً بك يا باشمهندس أحمد، السيستم يعمل بصلاحيات المدير الكاملة.")

elif choice == "👥 2. إدارة المستخدمين والصلاحيات (أنت المسؤول)":
    st.header("👥 لوحة التحكم في حسابات المستخدمين والمندوبين")
    st.write("من هنا يمكنك إضافة مستخدم جديد (مندوب أو مدير فرعي) وتحديد الرقم السري الخاص به:")
    
    with st.form("add_user_form"):
        col_u1, col_u2 = st.columns(2)
        with col_u1:
            new_username = st.text_input("اسم المستخدم للدخول (بالإنجليزية بدون مسافات مثل: delegate3)")
            new_fullname = st.text_input("الاسم بالكامل (مثل: محمود المندوب الجديد)")
        with col_u2:
            new_password = st.text_input("الرقم السري", type="password")
            new_role = st.selectbox("نوع الصلاحية", ["Delegate (مندوب مبيعات)", "Admin (مدير نظام)"])
            
        save_user_btn = st.form_submit_button("إضافة الحساب الجديد للنظام")
        if save_user_btn:
            if new_username.strip() and new_password.strip():
                role_val = "Admin" if "Admin" in new_role else "Delegate"
                st.session_state.users_db[new_username.strip()] = {
                    "password": new_password.strip(),
                    "name": new_fullname.strip() if new_fullname else new_username,
                    "role": role_val
                }
                if role_val == "Delegate":
                    st.session_state.delegates_custody[new_fullname.strip() if new_fullname else new_username] = 0.0
                st.success(f"تم إنشاء حساب للمستخدم ({new_username}) بنجاح!")
            else:
                st.error("الرجاء إدخال اسم المستخدم والرقم السري بشكل صحيح.")

    st.markdown("---")
    st.subheader("قائمة المستخدمين الحاليين بالسيستم:")
    users_list = []
    for uname, udata in st.session_state.users_db.items():
        users_list.append({"اسم المستخدم": uname, "الاسم الظاهري": udata["name"], "الصلاحية": "مدير" if udata["role"]=="Admin" else "مندوب"})
    st.dataframe(pd.DataFrame(users_list), use_container_width=True)

elif choice == "👤 حساب المندوب (تسجيل مبيعات وعُهدة)":
    delegate_name = st.session_state.user_display_name
    st.header(f"👤 لوحة المندوب: {delegate_name}")
    st.write(f"العهدة النقدية الحالية بحوزتك: `{st.session_state.delegates_custody.get(delegate_name, 0.0)}` جنيه")
    
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

elif choice == "🛒 3. المشتريات والموردين":
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

elif choice == "💰 4. المبيعات والعملاء":
    st.header("💰 إدارة المبيعات العامة للشركة")
    if st.session_state.sales:
        st.dataframe(pd.DataFrame(st.session_state.sales), use_container_width=True)
    else:
        st.info("لا توجد مبيعات مسجلة حتى الآن.")

elif choice == "⚙️ 5. المخازن والتشغيل (خام ومتغربل)":
    st.header("⚙️ إدارة خطوط الإنتاج والغربلة")
    with st.form("production_line_form"):
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            batch_no = st.text_input("رقم التشغيلة", "BATCH-1")
            raw_withdrawn = st.number_input("الكمية المسحوبة من الخام (كجم)", min_value=1.0, max_value=float(st.session_state.raw_stock) if st.session_state.raw_stock > 0 else 100.0, value=1000.0)
            raw_purchase_cost = st.number_input("تكلفة شراء الخام المسحوب (جنيه)", value=30000.0)
            proc_cost = st.number_input("مصاريف الغربلة والتعبئة (جنيه)", value=1500.0)
        with col_g2:
            ready_output = st.number_input("الكمية الناتجة متغربلة وجاهزة (كجم)", value=900.0)
            waste_rev = st.number_input("إيراد بيع الهالك/التبن (جنيه)", value=500.0)
            
            waste_amt = raw_withdrawn - ready_output
            net_batch_cost = (raw_purchase_cost + proc_cost) - waste_rev
            cost_per_kg = net_batch_cost / ready_output if ready_output > 0 else 0
            
        confirm_production = st.form_submit_button("اعتماد التشغيلة")
        if confirm_production:
            if raw_withdrawn > st.session_state.raw_stock:
                st.error("الكمية المسحوبة أكبر من المخزون الخام!")
            else:
                st.session_state.raw_stock -= raw_withdrawn
                st.session_state.ready_stock += ready_output
                st.session_state.production.append({"التشغيلة": batch_no, "الخام المسحوب": raw_withdrawn, "المتغربل": ready_output, "الهالك": waste_amt, "تكلفة الكيلو": round(cost_per_kg, 2)})
                st.success("تم تشغيل خط الغربلة وتحديث المخازن بنجاح!")

    if st.session_state.production:
        st.dataframe(pd.DataFrame(st.session_state.production), use_container_width=True)

elif choice == "💸 6. المصروفات والأرباح":
    st.header("💸 المصروفات التشغيلية وشخصية")
    with st.form("expense_form"):
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            exp_type = st.selectbox("نوع المصروف", ["شحن وتوزيع", "إيجار", "بنزين وسولار", "مصاريف غربلة", "مصروفات شخصية"])
            exp_desc = st.text_input("البيان")
        with col_e2:
            exp_amount = st.number_input("المبلغ (جنيه)", value=500.0)
            exp_source = st.selectbox("مدفوع من:", ["الخزنة النقدية", "فودافون كاش", "حساب بنكي"])
        save_exp = st.form_submit_button("تسجيل المصروف")
        if save_exp:
            st.session_state.expenses.append({"التصنيف": exp_type, "البيان": exp_desc, "المبلغ": exp_amount, "المصدر": exp_source})
            st.success("تم تسجیل المصروف بنجاح!")

    if st.session_state.expenses:
        st.dataframe(pd.DataFrame(st.session_state.expenses), use_container_width=True)

elif choice == "🏦 7. الخزنة والبنوك وفودافون كاش":
    st.header("🏦 إدارة الخزنة والبنوك وفودافون كاش")
    col_b1, col_b2, col_b3 = st.columns(3)
    col_b1.metric("💵 رصيد الخزنة", f"{st.session_state.cash_balance:,.2f} جنيه")
    col_b2.metric("📱 فودافون كاش", f"{st.session_state.vodafone_cash:,.2f} جنيه")
    col_b3.metric("💳 رصيد البنوك", f"{st.session_state.bank_balance:,.2f} جنيه")

elif choice == "🔒 8. إقفال اليوم والحسابات الختامية":
    st.header("🔒 إقفال اليوم المالي (للإدارة فقط)")
    with st.form("closing_form"):
        actual_cash = st.number_input("العد الفعلي للنقدية بالخزنة:", value=float(st.session_state.cash_balance))
        do_closing = st.form_submit_button("اعتماد إقفال اليوم")
        if do_closing:
            st.success("تم إقفال اليوم المالي بنجاح وحفظ الحسابات الختامية.")

elif choice == "📊 9. التقارير والطباعة الشاملة":
    st.header("📊 التقارير الشاملة")
    st.write(f"- رصيد بذور الخام: **{st.session_state.raw_stock:,.1f} كجم**")
    st.write(f"- رصيد بذور جاهزة: **{st.session_state.ready_stock:,.1f} كجم**")

elif choice == "⚙️ 10. إعدادات النظام والتحكم":
    st.header("⚙️ إعدادات النظام وتصفير البيانات")
    if st.button("🔄 تصفير السيستم بالكامل"):
        st.session_state.raw_stock = 0.0
        st.session_state.ready_stock = 0.0
        st.success("تم تصفير النظام.")
