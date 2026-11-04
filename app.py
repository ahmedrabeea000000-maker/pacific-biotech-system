import streamlit as st
import pandas as pd

# إعداد الصفحة وتوسيع العرض
st.set_page_config(page_title="شركة باسفيك بايوتك للتقاوي", layout="wide")

# ---------------------------------------------------------
# تهيئة قاعدة البيانات والـ Session State
# ---------------------------------------------------------
if 'cash_balance' not in st.session_state:
    st.session_state.cash_balance = 50000.0 
if 'bank_balance' not in st.session_state:
    st.session_state.bank_balance = 120000.0 
if 'vodafone_cash' not in st.session_state:
    st.session_state.vodafone_cash = 15000.0 

# مخزن الأصناف والأرصدة الافتتاحية
if 'items_inventory' not in st.session_state:
    st.session_state.items_inventory = {
        "ألفالفا Cuf101": {"raw_qty": 10000.0, "ready_qty": 3000.0},
        "بذور سيريفير": {"raw_qty": 5000.0, "ready_qty": 2000.0}
    }

if 'purchases' not in st.session_state:
    st.session_state.purchases = []
if 'sales' not in st.session_state:
    st.session_state.sales = []
if 'production' not in st.session_state:
    st.session_state.production = []
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# إدارة المستخدمين
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
# شاشة تسجيل الدخول النظيفة تماماً
# ---------------------------------------------------------
if not st.session_state.logged_in:
    st.title("🌱 شركة باسفيك بايوتك للتقاوي - تسجيل الدخول")
    st.markdown("---")
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.subheader("🔐 يرجى تسجيل الدخول للبدء")
        
        # استخدام مفاتيح فريدة ومنع التعبئة التلقائية المزعجة
        user_input = st.text_input("اسم المستخدم (Username)", value="", key="login_user")
        pass_input = st.text_input("الرقم السري (Password)", type="password", value="", key="login_pass")
        
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
    st.stop()

# ---------------------------------------------------------
# الواجهة الرئيسية الاحترافية بعد الدخول
# ---------------------------------------------------------
st.title("🌱 شركة باسفيك بايوتك للتقاوي للاستيراد والتصدير")
st.sidebar.success(f"مرحباً: {st.session_state.user_display_name}")

if st.sidebar.button("تسجيل الخروج 🚪"):
    st.session_state.logged_in = False
    st.session_state.user_role = ""
    st.rerun()

st.sidebar.markdown("---")

if st.session_state.user_role == "Admin":
    menu = [
        "📊 لوحة المؤشرات العامة",
        "📦 إدارة الأصناف والمخازن",
        "👥 إدارة المندوبين",
        "🛒 المشتريات والموردين",
        "💰 فواتير المبيعات",
        "⚙️ خطوط الغربلة والتشغيل",
        "💸 المصروفات والأرباح",
        "🏦 الخزنة والبنوك",
        "🔒 إقفال اليوم",
        "⚙️ إعدادات النظام"
    ]
else:
    menu = [
        "👤 حساب المندوب (تسجيل مبيعات)"
    ]

choice = st.sidebar.selectbox("القائمة الرئيسية للسيستم", menu)
st.markdown("---")

# ---------------------------------------------------------
# 1. لوحة المؤشرات العامة
# ---------------------------------------------------------
if choice == "📊 لوحة المؤشرات العامة":
    st.header("📊 لوحة المؤشرات والتقارير المالية والمخزنية الشاملة")
    
    m1, m2, m3, m4 = st.columns(4)
    total_sales = sum([s['الإجمالي'] for s in st.session_state.sales])
    total_purchases = sum([p['الإجمالي'] for p in st.session_state.purchases])
    
    m1.metric("إجمالي المبيعات", f"{total_sales:,.2f} جنيه")
    m2.metric("إجمالي المشتريات", f"{total_purchases:,.2f} جنيه")
    m3.metric("رصيد الخزنة النقدية", f"{st.session_state.cash_balance:,.2f} جنيه")
    m4.metric("رصيد فودافون كاش", f"{st.session_state.vodafone_cash:,.2f} جنيه")

    st.markdown("---")
    
    col_dash1, col_dash2 = st.columns(2)
    with col_dash1:
        st.subheader("📦 ملخص أرصدة المخازن لكل صنف")
        stock_summary = []
        for item, qtys in st.session_state.items_inventory.items():
            stock_summary.append({"الصنف": item, "رصيد الخام (كجم)": qtys["raw_qty"], "رصيد الجاهز (كجم)": qtys["ready_qty"]})
        if stock_summary:
            st.dataframe(pd.DataFrame(stock_summary), use_container_width=True)
        else:
            st.info("لا توجد أصناف مسجلة.")
            
    with col_dash2:
        st.subheader("⚡ اختصارات العمليات السريعة")
        if st.button("➕ إضافة فاتورة مبيعات جديدة فوراً"):
            st.warning("انتقل من القائمة الجانبية إلى (فواتير المبيعات).")
        if st.button("⚙️ تشغيل أمر غربلة جديد"):
            st.warning("انتقل من القائمة الجانبية إلى (خطوط الغربلة والتشغيل).")

# ---------------------------------------------------------
# 2. إدارة الأصناف والمخازن
# ---------------------------------------------------------
elif choice == "📦 إدارة الأصناف والمخازن":
    st.header("📦 إدارة الأصناف والأرصدة الابتدائية")
    
    with st.form("add_item_form"):
        col_i1, col_i2, col_i3 = st.columns(3)
        with col_i1:
            new_item_name = st.text_input("اسم صنف البذور الجديد")
        with col_i2:
            init_raw = st.number_input("الرصيد الابتدائي للخام (كجم)", min_value=0.0, value=1000.0)
        with col_i3:
            init_ready = st.number_input("الرصيد الابتدائي للجاهز (كجم)", min_value=0.0, value=500.0)
            
        if st.form_submit_button("حفظ وإضافة الصنف"):
            if new_item_name.strip():
                st.session_state.items_inventory[new_item_name.strip()] = {"raw_qty": init_raw, "ready_qty": init_ready}
                st.success(f"تم إضافة الصنف ({new_item_name}) بنجاح!")
            else:
                st.error("برجاء إدخال اسم صنف صحيح.")

    st.markdown("---")
    st.subheader("قائمة الأصناف الحالية:")
    items_list = [{"اسم الصنف": k, "الخام المتاح (كجم)": v["raw_qty"], "الجاهز المتاح (كجم)": v["ready_qty"]} for k, v in st.session_state.items_inventory.items()]
    st.dataframe(pd.DataFrame(items_list), use_container_width=True)

# ---------------------------------------------------------
# 3. إدارة المندوبين
# ---------------------------------------------------------
elif choice == "👥 إدارة المندوبين":
    st.header("👥 إدارة المستخدمين والمندوبين")
    
    with st.form("user_mgmt_form"):
        col_u1, col_u2 = st.columns(2)
        with col_u1:
            u_user = st.text_input("اسم المستخدم للدخول (مثل: delegate3)")
            u_name = st.text_input("الاسم بالكامل للمندوب")
        with col_u2:
            u_pass = st.text_input("الرقم السري", type="password")
            u_role = st.selectbox("الصلاحية", ["Delegate (مندوب مبيعات)", "Admin (مدير نظام)"])
            
        if st.form_submit_button("إضافة المستخدم"):
            if u_user.strip() and u_pass.strip():
                r_val = "Admin" if "Admin" in u_role else "Delegate"
                st.session_state.users_db[u_user.strip()] = {"password": u_pass.strip(), "name": u_name.strip() or u_user, "role": r_val}
                if r_val == "Delegate":
                    st.session_state.delegates_custody[u_name.strip() or u_user] = 0.0
                st.success(f"تم إنشاء حساب ({u_user}) بنجاح!")
            else:
                st.error("برجاء إدخال البيانات كاملة.")

    st.markdown("---")
    user_to_delete = st.selectbox("حذف مندوب أو مستخدم", list(st.session_state.users_db.keys()))
    if st.button("🗑️ حذف المستخدم"):
        if user_to_delete == "ahmedrabeea":
            st.error("لا يمكن حذف المدير الأساسي!")
        else:
            del st.session_state.users_db[user_to_delete]
            st.success("تم الحذف بنجاح.")
            st.rerun()

# ---------------------------------------------------------
# 4. المشتريات والموردين
# ---------------------------------------------------------
elif choice == "🛒 المشتريات والموردين":
    st.header("🛒 فواتير المشتريات والموردين")
    if not st.session_state.items_inventory:
        st.warning("⚠️ يرجى إضافة أصناف أولاً من قسم (إدارة الأصناف والمخازن).")
    else:
        with st.form("purchase_form"):
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                supplier = st.text_input("اسم المورد")
                item_choice = st.selectbox("اختر الصنف", list(st.session_state.items_inventory.keys()))
                p_type = st.radio("نوع المشتريات", ["بذرة خام (تحتاج غربلة)", "بذرة جاهزة"])
            with col_p2:
                qty = st.number_input("الكمية (كجم)", min_value=1.0, value=1000.0)
                price = st.number_input("سعر الكيلو (جنيه)", min_value=0.1, value=40.0)
                shipping = st.number_input("تكاليف الشحن (جنيه)", min_value=0.0, value=500.0)
                pay_status = st.selectbox("حالة السداد", ["نقداً", "آجل"])
                
            tot_p = (qty * price) + shipping
            st.markdown(f"### *إجمالي الفاتورة:* {tot_p:,.2f} جنيه")
            
            if st.form_submit_button("حفظ فاتورة المشتريات"):
                if "خام" in p_type:
                    st.session_state.items_inventory[item_choice]["raw_qty"] += qty
                else:
                    st.session_state.items_inventory[item_choice]["ready_qty"] += qty
                st.session_state.purchases.append({"المورد": supplier, "الصنف": item_choice, "النوع": p_type, "الكمية": qty, "الإجمالي": tot_p})
                st.success("تم الحفظ وتحديث المخزن بنجاح!")

        if st.session_state.purchases:
            st.dataframe(pd.DataFrame(st.session_state.purchases), use_container_width=True)

# ---------------------------------------------------------
# 5. المبيعات
# ---------------------------------------------------------
elif choice == "💰 فواتير المبيعات":
    st.header("💰 تسجيل فواتير المبيعات والعملاء")
    if not st.session_state.items_inventory:
        st.warning("⚠️ لا توجد أصناف متاحة.")
    else:
        with st.form("sales_form"):
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                cust_name = st.text_input("اسم العميل")
                item_choice = st.selectbox("اختر الصنف (من المخزن الجاهز)", list(st.session_state.items_inventory.keys()))
                sale_qty = st.number_input("الكمية المباعة (كجم)", min_value=1.0, value=100.0)
            with col_s2:
                sale_price = st.number_input("سعر بيع الكيلو (جنيه)", min_value=1.0, value=120.0)
                pay_method = st.selectbox("طريقة التحصيل", ["نقدي للصندوق", "فودافون كاش", "تحويل بنكي", "آجل"])
                
            tot_s = sale_qty * sale_price
            st.markdown(f"### *إجمالي الفاتورة:* {tot_s:,.2f} جنيه")
            
            if st.form_submit_button("اعتماد البيع وخصم المخزن"):
                avail = st.session_state.items_inventory[item_choice]["ready_qty"]
                if sale_qty > avail:
                    st.error(f"الكمية أكبر من المخزن الجاهز المتاح ({avail} كجم)!")
                else:
                    st.session_state.items_inventory[item_choice]["ready_qty"] -= sale_qty
                    if pay_method == "نقدي للصندوق":
                        st.session_state.cash_balance += tot_s
                    elif pay_method == "فودافون كاش":
                        st.session_state.vodafone_cash += tot_s
                    st.session_state.sales.append({"العميل": cust_name, "الصنف": item_choice, "الكمية": sale_qty, "الإجمالي": tot_s, "الطريقة": pay_method})
                    st.success("تم البيع بنجاح!")

        if st.session_state.sales:
            st.dataframe(pd.DataFrame(st.session_state.sales), use_container_width=True)

# ---------------------------------------------------------
# 6. خطوط الغربلة
# ---------------------------------------------------------
elif choice == "⚙️ خطوط الغربلة والتشغيل":
    st.header("⚙️ تشغيل خطوط الغربلة وحساب الهالك والتكلفة")
    if not st.session_state.items_inventory:
        st.warning("⚠️ لا توجد أصناف مسجلة.")
    else:
        with st.form("production_form"):
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                batch_no = st.text_input("رقم التشغيلة", "BATCH-01")
                item_choice = st.selectbox("اختر صنف البذور", list(st.session_state.items_inventory.keys()))
                max_raw = float(st.session_state.items_inventory[item_choice]["raw_qty"])
                st.info(f"🌾 الخام المتاح للصنف: {max_raw:,.1f} كجم")
                
                raw_withdrawn = st.number_input("الكمية المسحوبة من الخام (كجم)", min_value=0.0, max_value=max(max_raw, 0.1), value=min(1000.0, max_raw))
                raw_cost = st.number_input("تكلفة الخام (جنيه)", value=30000.0)
                proc_cost = st.number_input("مصاريف الغربلة (جنيه)", value=1500.0)
            with col_g2:
                ready_out = st.number_input("الكمية الناتجة جاهزة (كجم)", min_value=0.0, value=900.0)
                waste_rev = st.number_input("إيراد بيع التبن/الهالك (جنيه)", value=500.0)
                
                waste_qty = raw_withdrawn - ready_out
                net_c = (raw_cost + proc_cost) - waste_rev
                cost_per_kg = net_c / ready_out if ready_out > 0 else 0
                
                st.markdown(f"""
                ---
                * *الهالك / الفاقد:* {waste_qty:,.1f} كجم
                * *تكلفة الكيلو الجاهز:* {cost_per_kg:,.2f} جنيه/كجم
                """)
                
            if st.form_submit_button("اعتماد التشغيلة"):
                if raw_withdrawn > max_raw:
                    st.error("الكمية المسحوبة أكبر من رصيد الخام المتاح!")
                else:
                    st.session_state.items_inventory[item_choice]["raw_qty"] -= raw_withdrawn
                    st.session_state.items_inventory[item_choice]["ready_qty"] += ready_out
                    st.session_state.production.append({"التشغيلة": batch_no, "الصنف": item_choice, "الخام": raw_withdrawn, "الجاهز": ready_out, "الهالك": waste_qty, "تكلفة الكيلو": round(cost_per_kg, 2)})
                    st.success("تمت التشغيلة بنجاح!")

        if st.session_state.production:
            st.dataframe(pd.DataFrame(st.session_state.production), use_container_width=True)

# ---------------------------------------------------------
# باقي الأقسام
# ---------------------------------------------------------
elif choice == "💸 المصروفات والأرباح":
    st.header("💸 المصروفات التشغيلية")
    with st.form("exp_form"):
        e_type = st.selectbox("النوع", ["شحن", "إيجار", "بنزين", "مصاريف غربلة", "شخصية"])
        e_desc = st.text_input("البيان")
        e_amt = st.number_input("المبلغ (جنيه)", value=500.0)
        if st.form_submit_button("تسجيل المصروف"):
            st.session_state.expenses.append({"النوع": e_type, "البيان": e_desc, "المبلغ": e_amt})
            st.success("تم التسجيل.")
    if st.session_state.expenses:
        st.dataframe(pd.DataFrame(st.session_state.expenses), use_container_width=True)

elif choice == "🏦 الخزنة والبنوك":
    st.header("🏦 إدارة الخزنة والبنوك")
    c1, c2, c3 = st.columns(3)
    c1.metric("💵 رصيد الخزنة", f"{st.session_state.cash_balance:,.2f} جنيه")
    c2.metric("📱 فودافون كاش", f"{st.session_state.vodafone_cash:,.2f} جنيه")
    c3.metric("💳 البنوك", f"{st.session_state.bank_balance:,.2f} جنيه")

elif choice == "🔒 إقفال اليوم":
    st.header("🔒 إقفال اليوم المالي")
    if st.button("اعتماد الإقفال"):
        st.success("تم إقفال اليوم بنجاح.")

elif choice == "⚙️ إعدادات النظام":
    st.header("⚙️ إعدادات النظام وتصفير البيانات")
    if st.button("🔄 تصفير السيستم بالكامل"):
        st.session_state.items_inventory = {}
        st.success("تم التصفير.")

elif choice == "👤 حساب المندوب (تسجيل مبيعات)":
    d_name = st.session_state.user_display_name
    st.header(f"👤 لوحة المندوب: {d_name}")
    st.write(f"العهدة النقدية: {st.session_state.delegates_custody.get(d_name, 0.0)} جنيه")
    
    if not st.session_state.items_inventory:
        st.warning("لا توجد أصناف متاحة.")
    else:
        with st.form("del_form"):
            c_cust = st.text_input("اسم العميل")
            c_item = st.selectbox("اختر الصنف الجاهز", list(st.session_state.items_inventory.keys()))
            c_qty = st.number_input("الكمية (كجم)", value=50.0)
            c_price = st.number_input("سعر الكيلو", value=120.0)
            c_pay = st.selectbox("التحصيل", ["نقدي للصندوق", "فودافون كاش", "آجل"])
            
            if st.form_submit_button("تسجيل البيع وتحصيل المبلغ"):
                tot_d = c_qty * c_price
                avail = st.session_state.items_inventory[c_item]["ready_qty"]
                if c_qty > avail:
                    st.error(f"الكمية أكبر من المخزون الجاهز المتاح ({avail} كجم)!")
                else:
                    st.session_state.items_inventory[c_item]["ready_qty"] -= c_qty
                    st.session_state.sales.append({"المندوب": d_name, "العميل": c_cust, "الصنف": c_item, "الكمية": c_qty, "الإجمالي": tot_d, "الطريقة": c_pay})
                    st.success(f"تم البيع بنجاح بقيمة {tot_d:,.2f} جنيه!")
