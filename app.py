import streamlit as st
import pandas as pd

# إعداد الصفحة وتوسيع العرض
st.set_page_config(page_title="شركة باسفيك بايوتك للتقاوي", layout="wide")

# تهيئة قاعدة البيانات المؤقتة في الـ Session State
if 'raw_stock' not in st.session_state:
    st.session_state.raw_stock = 15000.0  # كجم بذرة خام
if 'ready_stock' not in st.session_state:
    st.session_state.ready_stock = 5000.0   # كجم بذرة جاهزة
if 'purchases' not in st.session_state:
    st.session_state.purchases = []
if 'production' not in st.session_state:
    st.session_state.production = []

# 1. عنوان الصفحة الرئيسي باسم الشركة فقط
st.title("🌱 شركة باسفيك بايوتك للتقاوي للاستيراد والتصدير")
st.markdown("---")

# القائمة الجانبية للنظام شاملة الإعدادات
menu = [
    "📊 لوحة التقارير والأرباح الشاملة",
    "🛒 فواتير المشتريات والموردين",
    "⚙️ خط الغربلة والإنتاج المربوط بالمخزن",
    "💰 فواتير المبيعات والعملاء",
    "💸 المصروفات والخزينة",
    "📅 التقفيل السنوي والتقارير المالية",
    "⚙️ إعدادات النظام والتحكم"
]

choice = st.sidebar.selectbox("اختر القسم", menu)

# ---------------------------------------------------------
# 1. لوحة التقارير والأرباح الشاملة (Dashboard)
# ---------------------------------------------------------
if choice == "📊 لوحة التقارير والأرباح الشاملة":
    st.header("📊 لوحة المؤشرات والتقارير المالية والمخزنية")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.selectbox("الفترة الزمنية / الدورية", ["الكل", "الشهر الحالي", "الربع السنوي", "السنة المالية الحالية"])
    with col_f2:
        st.selectbox("الفرع / المخزن", ["المخزن الرئيسي (كفر حكيم)", "خط الغربلة"])
    with col_f3:
        st.selectbox("العملة", ["جنيه مصري (EGP)", "دولار أمريكي (USD)"])

    st.markdown("---")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("رصيد المخزن الخام", f"{st.session_state.raw_stock:,.1f} كجم")
    m2.metric("رصيد المكتمل/الجاهز", f"{st.session_state.ready_stock:,.1f} كجم")
    m3.metric("إجمالي المشتريات", f"{len(st.session_state.purchases)} عملية")
    m4.metric("عمليات الغربلة والإنتاج", f"{len(st.session_state.production)} تشغيلة")

    st.markdown("---")

    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("📈 ملخص قائمة الدخل (الأرباح والخسائر)")
        df_pl = pd.DataFrame({
            "البند المالي": ["إيرادات المبيعات", "تكلفة البضاعة المباعة", "إجمالي مجمل الربح", "المصروفات التشغيلية", "صافي الربح الفعلي"],
            "القيمة (جنيه)": ["145,000", "98,000", "47,000", "7,500", "39,500"]
        })
        st.dataframe(df_pl, use_container_width=True)

    with col_right:
        st.subheader("📦 حالة أرصدة المخازن الحالية")
        df_stock = pd.DataFrame({
            "نوع البضاعة": ["بذور خام (تحت التجهيز)", "بذور جاهزة للمبيعات والتصدير"],
            "الكمية الحالية": [f"{st.session_state.raw_stock:,.1f} كجم", f"{st.session_state.ready_stock:,.1f} كجم"],
            "الحالة المخزنية": ["يحتاج غربلة", "جاهز للتعبئة والبيع"]
        })
        st.dataframe(df_stock, use_container_width=True)

# ---------------------------------------------------------
# 2. فواتير المشتريات والموردين
# ---------------------------------------------------------
elif choice == "🛒 فواتير المشتريات والموردين":
    st.header("🛒 تسجيل فاتورة مشتريات جديدة")
    
    with st.form("purchase_form"):
        col1, col2 = st.columns(2)
        with col1:
            supplier_name = st.text_input("اسم المورد")
            item_name = st.text_input("اسم البذرة (مثلاً: ألفالفا Cuf101 / سيريفير)")
            item_type = st.radio("نوع البضاعة المشتراة", ["بذرة خام (تحتاج غربلة)", "بذرة جاهزة (بدون غربلة)"])
        with col2:
            weight_kg = st.number_input("الوزن الإجمالي (كجم)", min_value=1.0, value=1000.0)
            price_per_kg = st.number_input("سعر الكيلو (جنيه)", min_value=0.1, value=15.0)
            total_price = weight_kg * price_per_kg
            st.markdown(f"### *إجمالي الفاتورة:* {total_price:,.2f} جنيه")
            
        submit_btn = st.form_submit_button("تسجيل الفاتورة وإضافة للمخزن")
        
        if submit_btn:
            if item_type == "بذرة خام (تحتاج غربلة)":
                st.session_state.raw_stock += weight_kg
            else:
                st.session_state.ready_stock += weight_kg
                
            st.session_state.purchases.append({
                "المورد": supplier_name,
                "الصنف": item_name,
                "النوع": item_type,
                "الوزن": weight_kg,
                "الإجمالي": total_price
            })
            st.success(f"تم تسجيل الفاتورة بنجاح وتحديث المخزن (+{weight_kg} كجم)!")

    if st.session_state.purchases:
        st.subheader("سجل الفواتير المشتراة")
        st.dataframe(pd.DataFrame(st.session_state.purchases), use_container_width=True)

# ---------------------------------------------------------
# 3. خط الغربلة والإنتاج المربوط بالمخزن
# ---------------------------------------------------------
elif choice == "⚙️ خط الغربلة والإنتاج المربوط بالمخزن":
    st.header("⚙️ تشغيل خط الغربلة وحساب التكلفة والهالك")
    st.write(f"🔒 *الرصيد المتاح من الخام في المخزن حالياً:* {st.session_state.raw_stock:,.1f} كجم")
    
    with st.form("production_form"):
        col1, col2 = st.columns(2)
        with col1:
            batch_code = st.text_input("رقم التشغيلة / اللوط", "B-101")
            raw_input_kg = st.number_input("الكمية المسحوبة من المخزن الخام (كجم)", min_value=1.0, max_value=float(st.session_state.raw_stock) if st.session_state.raw_stock > 0 else 100.0, value=min(1000.0, float(st.session_state.raw_stock)))
            raw_cost_total = st.number_input("تكلفة الشراء الأصلية للدفعة المسحوبة (جنيه)", min_value=0.0, value=15000.0)
            process_cost = st.number_input("مصاريف الغربلة والنقل والشكاير (جنيه)", min_value=0.0, value=1000.0)
            
        with col2:
            ready_output_kg = st.number_input("الكمية الصافية الجاهزة الناتجة (كجم)", min_value=0.0, value=900.0)
            waste_revenue = st.number_input("إيراد بيع التبن / الهالك (إن وجد) (جنيه)", min_value=0.0, value=300.0)
            
            waste_kg = raw_input_kg - ready_output_kg
            net_cost = (raw_cost_total + process_cost) - waste_revenue
            cost_per_ready_kg = net_cost / ready_output_kg if ready_output_kg > 0 else 0
            
            st.markdown(f"""
            ---
            * *الهالك / الفاقد:* {waste_kg:,.1f} كجم
            * *صافي تكلفة التشغيلة:* {net_cost:,.2f} جنيه
            * 💥 *تكلفة الكيلو الجاهز الفعلي:* {cost_per_ready_kg:,.2f} جنيه/كجم
            """)

        submit_prod = st.form_submit_button("اعتماد التشغيلة (خصم الخام وإضافة الجاهز)")
        
        if submit_prod:
            if raw_input_kg > st.session_state.raw_stock:
                st.error("الكمية المسحوبة أكبر من المتاح في مخزن الخام!")
            else:
                st.session_state.raw_stock -= raw_input_kg
                st.session_state.ready_stock += ready_output_kg
                
                st.session_state.production.append({
                    "رقم التشغيلة": batch_code,
                    "الخام المسحوب (كجم)": raw_input_kg,
                    "المنتج الجاهز (كجم)": ready_output_kg,
                    "الهالك (كجم)": waste_kg,
                    "تكلفة الكيلو الجاهز": round(cost_per_ready_kg, 2)
                })
                st.success(f"تم بنجاح! خصم {raw_input_kg} كجم خام، وإضافة {ready_output_kg} كجم جاهز للمخزن.")

    if st.session_state.production:
        st.subheader("سجل عمليات الغربلة والإنتاج")
        st.dataframe(pd.DataFrame(st.session_state.production), use_container_width=True)

# ---------------------------------------------------------
# 4 & 5 & 6. الأقسام الأخرى
# ---------------------------------------------------------
elif choice == "💰 فواتير المبيعات والعملاء":
    st.header("💰 قسم فواتير المبيعات والعملاء")
    st.write(f"🔒 *الرصيد المتاح للبيع من البضاعة الجاهزة:* {st.session_state.ready_stock:,.1f} كجم")

elif choice == "💸 المصروفات والخزينة":
    st.header("💸 المصروفات اليومية وحركة الخزينة")

elif choice == "📅 التقفيل السنوي والتقارير المالية":
    st.header("📅 الحسابات الختامية والتقفيل السنوي لشركة باسفيك بايوتك")

# ---------------------------------------------------------
# 7. إعدادات النظام والتحكم (لإلغاء العمليات وضبط الأرصدة)
# ---------------------------------------------------------
elif choice == "⚙️ إعدادات النظام والتحكم":
    st.header("⚙️ لوحة تحكم وإعدادات النظام")
    st.warning("⚠️ تحذير: من هذه اللوحة يمكنك تعديل الأرصدة الافتتاحية أو مسح وإلغاء العمليات المسجلة.")

    col_set1, col_set2 = st.columns(2)
    with col_set1:
        st.subheader("📦 تعديل الأرصدة الافتتاحية للمخازن")
        new_raw_init = st.number_input("تعديل رصيد المخزن الخام الحالي (كجم)", value=float(st.session_state.raw_stock))
        new_ready_init = st.number_input("تعديل رصيد المخزن الجاهز الحالي (كجم)", value=float(st.session_state.ready_stock))
        
        if st.button("حفظ تعديلات الأرصدة"):
            st.session_state.raw_stock = new_raw_init
            st.session_state.ready_stock = new_ready_init
            st.success("تم تحديث الأرصدة بنجاح!")

    with col_set2:
        st.subheader("🗑️ إلغاء ومسح العمليات")
        if st.button("مسح كل سجلات فواتير المشتريات"):
            st.session_state.purchases = []
            st.success("تم تفريغ سجلات المشتريات بالكامل.")
            
        if st.button("مسح كل سجلات خط الغربلة والإنتاج"):
            st.session_state.production = []
            st.success("تم تفريغ سجلات الإنتاج بالكامل.")
            
        if st.button("🔄 إعادة ضبط المصنع (تصفير السيستم بالكامل)"):
            st.session_state.raw_stock = 0.0
            st.session_state.ready_stock = 0.0
            st.session_state.purchases = []
            st.session_state.production = []
            st.success("تم تصفير النظام وإعادة ضبطه من الصفر بنجاح!")
