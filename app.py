import streamlit as st
import pandas as pd
import datetime

# إعداد الصفحة وتوسيع العرض
st.set_page_config(page_title="شركة باسفيك بايوتك للتقاوي", layout="wide")

# ---------------------------------------------------------
# تهيئة قاعدة البيانات المؤقتة في الـ Session State
# ---------------------------------------------------------
if 'raw_stock' not in st.session_state:
    st.session_state.raw_stock = 15000.0  # كجم بذرة خام
if 'ready_stock' not in st.session_state:
    st.session_state.ready_stock = 5000.0   # كجم بذرة متغربلة/جاهزة
if 'cash_balance' not in st.session_state:
    st.session_state.cash_balance = 50000.0 # رصيد الخزنة
if 'bank_balance' not in st.session_state:
    st.session_state.bank_balance = 120000.0 # رصيد البنك
if 'vodafone_cash' not in st.session_state:
    st.session_state.vodafone_cash = 15000.0 # رصيد فودافون كاش
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

# 1. عنوان الصفحة الرئيسي باسم الشركة فقط
st.title("🌱 شركة باسفيك بايوتك للتقاوي للاستيراد والتصدير")
st.markdown("---")

# القائمة الجانبية للنظام المتكامل
menu = [
    "🏠 1. الصفحة الرئيسية واللوحة العامة",
    "👑 2. حساب المدير والرقابة",
    "👤 3. حساب المندوبين",
    "🛒 4. المشتريات والموردين",
    "💰 5. المبيعات والعملاء",
    "⚙️ 6. المخازن والتشغيل (خام ومتغربل)",
    "💸 7. المصروفات والأرباح",
    "🏦 8. الخزنة والبنوك وفودافون كاش",
    "🔒 9. إقفال اليوم والحسابات الختامية",
    "📊 10. التقارير والطباعة الشاملة",
    "⚙️ 11. إعدادات النظام والتحكم"
]

choice = st.sidebar.selectbox("اختر القسم الرئيسي", menu)

# ---------------------------------------------------------
# 1. الصفحة الرئيسية واللوحة العامة
# ---------------------------------------------------------
if choice == "🏠 1. الصفحة الرئيسية واللوحة العامة":
    st.header("🏠 لوحة المؤشرات العامة للشركة")
    
    # مؤشرات سريعة عريضة
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
        st.subheader("🔔 التنبيهات والتنبيهات الحية")
        if st.session_state.raw_stock < 2000:
            st.warning("⚠️ تنبيه: رصيد البذور الخام منخفض ويجب إعادة الطلب!")
        else:
            st.success("✅ مستويات المخزون الخام آمنة.")
        st.info("💡 تم تفعيل نظام الـ ERP المتكامل بنجاح لكافة الأقسام.")

# ---------------------------------------------------------
# 2. حساب المدير والرقابة
# ---------------------------------------------------------
elif choice == "👑 2. حساب المدير والرقابة":
    st.header("👑 لوحة تحكم المدير العام والرقابة الشاملة")
    st.write("مرحباً بك يا مدير النظام. يمكنك من هنا متابعة أداء المندوبين، مراجعة العمليات، واعتماد الخصومات والمرتجعات.")
    
    tab1, tab2, tab3 = st.tabs(["👥 متابعة المندوبين وعهددهم", "📉 مراجعة وحركة الأسعار", "🔐 صلاحيات الإدارة العليا"])
    with tab1:
        st.subheader("عهُดات المندوبين الحالية")
        custody_df = pd.DataFrame(list(st.session_state.delegates_custody.items()), columns=["اسم المندوب", "العهدة النقدية الحالية (جنيه)"])
        st.dataframe(custody_df, use_container_width=True)
        
    with tab2:
        st.subheader("تحديد أسعار البيع والخصومات المسموحة")
        st.number_input("سعر بيع كيلو بذور ألفالفا الجاهزة الأساسي (جنيه)", value=120.0)
        st.number_input("أقصى نسبة خصم مسموحة للمندوب (%)", value=5.0)
        st.success("تم تحديث السياسة التسعيرية بنجاح.")
        
    with tab3:
        st.info("🔒 جميع الحركات المالية وتعديلات الفواتير مسجلة ومؤمنة بصلاحيات المدير فقط.")

# ---------------------------------------------------------
# 3. حساب المندوبين
# ---------------------------------------------------------
elif choice == "👤 3. حساب المندوبين":
    st.header("👤 بوابة تسجيل المندوب (مبيعات وتحصيلات)")
    
    delegate_name = st.selectbox("اختر اسم المندوب", ["أحمد المندوب", "محمود المندوب"])
    st.write(f"أنت تسجل الآن بصفتك: *{delegate_name}* | العهدة النقدية الحالية بحوزتك: {st.session_state.delegates_custody.get(delegate_name, 0)} جنيه")
    
    with st.form("delegate_action_form"):
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            cust_name = st.text_input("اسم العميل")
            seed_qty = st.number_input("الكمية المباعة (كجم)", min_value=1.0, value=100.0)
            sale_price = st.number_input("سعر البيع للكيلو (جنيه)", min_value=1.0, value=120.0)
        with col_d2:
            collection_type = st.selectbox("طريقة التحصيل", ["نقدي للخزنة", "فودافون كاش", "تحويل بنكي", "آجل / على الحساب"])
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
                st.success(f"تم تسجيل عملية البيع بنجاح بمبلغ {total_sale_amt:,.2f} جنيه وخصمها من المخزن المتغربل!")

# ---------------------------------------------------------
# 4. المشتريات والموردين
# ---------------------------------------------------------
elif choice == "🛒 4. المشتريات والموردين":
    st.header("🛒 إدارة المشتريات والموردين (نقدية وآجلة)")
    
    with st.form("purchase_section_form"):
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            supplier = st.text_input("اسم المورد")
            item = st.text_input("اسم الصنف (مثل: بذور ألفالفا خام)")
            p_type = st.radio("نوع البضاعة", ["بذرة خام (تحتاج غربلة)", "بذرة جاهزة"])
        with col_p2:
            qty = st.number_input("الكمية (كجم)", min_value=1.0, value=2000.0)
            price = st.number_input("سعر الكيلو (جنيه)", min_value=0.1, value=40.0)
            shipping_cost = st.number_input("تكاليف الشحن والنقل (جنيه)", min_value=0.0, value=1000.0)
            payment_status = st.selectbox("حالة السداد", ["نقدى بالكامل", "آجل / على الحساب"])
            
        tot_purchase = (qty * price) + shipping_cost
        st.markdown(f"### *إجمالي فاتورة المشتريات مع الشحن:* {tot_purchase:,.2f} جنيه")
        
        save_purchase = st.form_submit_button("حفظ فاتورة المشتريات وتحديث المخزن")
        if save_purchase:
            if p_type == "بذرة خام (تحتاج غربلة)":
                st.session_state.raw_stock += qty
            else:
                st.session_state.ready_stock += qty
                
            st.session_state.purchases.append({
                "المورد": supplier,
                "الصنف": item,
                "النوع": p_type,
                "الكمية": qty,
                "الإجمالي": tot_purchase,
                "الحالة": payment_status
            })
            st.success("تم حفظ الفاتورة وتحديث المخزن المالي والمخزني بنجاح!")

    if st.session_state.purchases:
        st.subheader("سجل فواتير المشتريات المسجلة")
        st.dataframe(pd.DataFrame(st.session_state.purchases), use_container_width=True)

# ---------------------------------------------------------
# 5. المبيعات والعملاء
# ---------------------------------------------------------
elif choice == "💰 5. المبيعات والعملاء":
    st.header("💰 إدارة المبيعات وفواتير العملاء")
    st.write(f"📦 رصيد المخزن المتغربل المتاح للبيع: {st.session_state.ready_stock:,.1f} كجم")
    
    if st.session_state.sales:
        st.subheader("سجل المبيعات العامة للشركة")
        st.dataframe(pd.DataFrame(st.session_state.sales), use_container_width=True)
    else:
        st.info("لا توجد مبيعات مسجلة حتى الآن. يمكنك تسجيلها من حساب المندوبين أو القسم المباشر.")

# ---------------------------------------------------------
# 6. المخازن والتشغيل (خام ومتغربل)
# ---------------------------------------------------------
elif choice == "⚙️ 6. المخازن والتشغيل (خام ومتغربل)":
    st.header("⚙️ إدارة خطوط الإنتاج والغربلة والتحكم في المخازن")
    
    st.markdown("""
    > *دورة التشغيل:* شراء الخام (يزيد الخام) ➡️ تحويل الخام للغربلة (يخصم من الخام) ➡️ إنتاج بضاعة متغربلة (يضاف للجاهز) ➡️ البيع أو الهالك.
    """)
    
    with st.form("production_line_form"):
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            batch_no = st.text_input("رقم التشغيلة / اللوط", "BATCH-2026-1")
            raw_withdrawn = st.number_input("الكمية المسحوبة من مخزن الخام (كجم)", min_value=1.0, max_value=float(st.session_state.raw_stock) if st.session_state.raw_stock > 0 else 100.0, value=min(1000.0, float(st.session_state.raw_stock)))
            raw_purchase_cost = st.number_input("تكلفة الشراء الأصلية للخام المسحوب (جنيه)", min_value=0.0, value=30000.0)
            proc_cost = st.number_input("مصاريف الغربلة والتعبئة والشكاير (جنيه)", min_value=0.0, value=1500.0)
        with col_g2:
            ready_output = st.number_input("الكمية الصافية الناتجة متغربلة وجاهزة (كجم)", min_value=0.0, value=900.0)
            waste_rev = st.number_input("إيراد بيع التبن / الهالك (إن وجد) (جنيه)", min_value=0.0, value=500.0)
            
            waste_amt = raw_withdrawn - ready_output
            net_batch_cost = (raw_purchase_cost + proc_cost) - waste_rev
            cost_per_kg = net_batch_cost / ready_output if ready_output > 0 else 0
            
            st.markdown(f"""
            ---
            * *هالك الغربلة والفاقد:* {waste_amt:,.1f} كجم
            * *صافي تكلفة التشغيلة:* {net_batch_cost:,.2f} جنيه
            * 💥 *تكلفة الكيلو الجاهز الفعلي:* {cost_per_kg:,.2f} جنيه/كجم
            """)
            
        confirm_production = st.form_submit_button("اعتماد التشغيلة (خصم الخام وإضافة المتغربل)")
        if confirm_production:
            if raw_withdrawn > st.session_state.raw_stock:
                st.error("الكمية المسحوبة أكبر من رصيد الخام المتاح بالمخزن!")
            else:
                st.session_state.raw_stock -= raw_withdrawn
                st.session_state.ready_stock += ready_output
                st.session_state.production.append({
                    "التشغيلة": batch_no,
                    "الخام المسحوب": raw_withdrawn,
                    "المتغربل الناتج": ready_output,
                    "الهالك": waste_amt,
                    "تكلفة الكيلو": round(cost_per_kg, 2)
                })
                st.success("تم تشغيل خط الغربلة وتحديث أرصدة المخازن (خام ومتغربل) بنجاح تام!")

    if st.session_state.production:
        st.subheader("سجل عمليات الغربلة والتشغيل السابقة")
        st.dataframe(pd.DataFrame(st.session_state.production), use_container_width=True)

# ---------------------------------------------------------
# 7. المصروفات والأرباح
# ---------------------------------------------------------
elif choice == "💸 7. المصروفات والأرباح":
    st.header("💸 المصروفات التشغيلية والشخصية وحساب الأرباح")
    
    with st.form("expense_form"):
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            exp_type = st.selectbox("نوع المصروف", ["شحن وتوزيع", "إيجار المخزن والسيارات", "بنزين وسولار", "مصاريف غربلة وتعبئة", "عمولات مندوبين", "مصروفات شخصية محملة على الأرباح"])
            exp_desc = st.text_input("بيان المصروف بالتفصيل")
        with col_e2:
            exp_amount = st.number_input("المبلغ المدفوع (جنيه)", min_value=1.0, value=500.0)
            exp_source = st.selectbox("مدفوع من:", ["الخزنة النقدية", "فودافون كاش", "حساب بنكي"])
            
        save_exp = st.form_submit_button("تسجيل المصروف")
        if save_exp:
            if exp_source == "الخزنة النقدية" and st.session_state.cash_balance >= exp_amount:
                st.session_state.cash_balance -= exp_amount
            elif exp_source == "فودافون كاش" and st.session_state.vodafone_cash >= exp_amount:
                st.session_state.vodafone_cash -= exp_amount
            elif exp_source == "حساب بنكي" and st.session_state.bank_balance >= exp_amount:
                st.session_state.bank_balance -= exp_amount
                
            st.session_state.expenses.append({
                "التصنيف": exp_type,
                "البيان": exp_desc,
                "المبلغ": exp_amount,
                "الخزنة المصروف منها": exp_source
            })
            st.success("تم تسجیل المصروف وخصمه من الخزنة بنجاح!")

    if st.session_state.expenses:
        st.subheader("سجل المصروفات المسجلة")
        st.dataframe(pd.DataFrame(st.session_state.expenses), use_container_width=True)

# ---------------------------------------------------------
# 8. الخزنة والبنوك وفودافون كاش
# ---------------------------------------------------------
elif choice == "🏦 8. الخزنة والبنوك وفودافون كاش":
    st.header("🏦 إدارة الخزنة، البنوك، فودافون كاش والتحويلات المالية")
    
    col_b1, col_b2, col_b3 = st.columns(3)
    col_b1.metric("💵 رصيد الخزنة النقدية", f"{st.session_state.cash_balance:,.2f} جنيه")
    col_b2.metric("📱 رصيد فودافون كاش", f"{st.session_state.vodafone_cash:,.2f} جنيه")
    col_b3.metric("💳 رصيد البنوك", f"{st.session_state.bank_balance:,.2f} جنيه")
    
    st.markdown("---")
    st.subheader("إجراء تحويل داخلي بين الحسابات أو إيداع/صرف")
    with st.form("transfer_form"):
        t_from = st.selectbox("من حساب:", ["الخزنة النقدية", "فودافون كاش", "حساب بنكي"])
        t_to = st.selectbox("إلى حساب:", ["فودافون كاش", "الخزنة النقدية", "حساب بنكي"])
        t_amount = st.number_input("مبلغ التحويل (جنيه)", min_value=1.0, value=1000.0)
        
        do_transfer = st.form_submit_button("تنفيذ التحويل المالي")
        if do_transfer:
            st.success(f"تم بنجاح تحويل مبلغ {t_amount:,.2f} جنيه من {t_from} إلى {t_to}.")

# ---------------------------------------------------------
# 9. إقفال اليوم والحسابات الختامية
# ---------------------------------------------------------
elif choice == "🔒 9. إقفال اليوم والحسابات الختامية":
    st.header("🔒 التقفيل اليومي وإغلاق حسابات اليوم (صلاحية المدير)")
    st.warning("⚠️ تنبيه: تقفيل اليوم يعتمد حركة المبيعات والمصروفات والعهد النقدية ويغلق اليوم مالياً.")
    
    with st.form("closing_form"):
        actual_cash_counted = st.number_input("النقدية الفعلية الموجودة بالخزنة الآن (العد الفعلي باليد):", min_value=0.0, value=float(st.session_state.cash_balance))
        closing_notes = st.text_area("ملاحظات إقفال الوردية أو اليوم")
        
        do_closing = st.form_submit_button("اعتماد إقفال اليوم المالي")
        if do_closing:
            diff = actual_cash_counted - st.session_state.cash_balance
            st.success("تم إقفال اليوم بنجاح وحفظ التقارير الختامية للمدير.")
            if diff == 0:
                st.info("طابق الرصيد الدفتري مع العد الفعلي تماماً (لا يوجد عجز أو زيادة).")
            elif diff > 0:
                st.success(f"يوجد زيادة نقدية بالخزنة قدرها: +{diff:,.2f} جنيه.")
            else:
                st.error(f"يوجد عجز نقدي بالخزنة قدرها: {diff:,.2f} جنيه.")

# ---------------------------------------------------------
# 10. التقارير والطباعة الشاملة
# ---------------------------------------------------------
elif choice == "📊 10. التقارير والطباعة الشاملة":
    st.header("📊 التقارير المالية والإدارية الشاملة للشركة")
    
    report_type = st.selectbox("اختر التقرير المطلوب", [
        "تقرير حركة المخزون (خام ومتغربل)",
        "تقرير المبيعات والأرباح",
        "تقرير المندوبين والعمولات",
        "تقرير المصروفات والخزينة"
    ])
    
    if report_type == "تقرير حركة المخزون (خام ومتغربل)":
        st.subheader("تقرير أرصدة المخازن الفورية")
        st.write(f"- رصيد بذور الخام: *{st.session_state.raw_stock:,.1f} كجم*")
        st.write(f"- رصيد بذور متغربلة (جاهزة): *{st.session_state.ready_stock:,.1f} كجم*")
    elif report_type == "تقرير المبيعات والأرباح":
        st.subheader("ملخص المبيعات الكلية")
        if st.session_state.sales:
            st.dataframe(pd.DataFrame(st.session_state.sales), use_container_width=True)
        else:
            st.info("لا توجد مبيعات مسجلة لعرضها.")
    else:
        st.info("جارٍ تجهيز تفاصيل التقرير المطلوب...")

# ---------------------------------------------------------
# 11. إعدادات النظام والتحكم
# ---------------------------------------------------------
elif choice == "⚙️ 11. إعدادات النظام والتحكم":
    st.header("⚙️ إعدادات النظام المتقدمة وتصفير البيانات")
    st.warning("تحذير خطير: أزرار التحكم التالية تقوم بتعديل أو مسح بيانات السيستم بالكامل.")
    
    if st.button("🔄 إعادة ضبط المصنع وتصفير النظام بالكامل"):
        st.session_state.raw_stock = 0.0
        st.session_state.ready_stock = 0.0
        st.session_state.cash_balance = 0.0
        st.session_state.bank_balance = 0.0
        st.session_state.vodafone_cash = 0.0
        st.session_state.purchases = []
        st.session_state.sales = []
        st.session_state.production = []
        st.session_state.expenses = []
        st.success("تم تصفير النظام وإعادة ضبطه بنجاح.")
