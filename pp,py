import streamlit as st
import pandas as pd

st.set_page_config(page_title="باسفيك بايوتك للتقاوي", layout="wide")

st.title("🌱 نظام إدارة وتكلفة غربلة البذور - شركة باسفيك بايوتك للتقاوي للاستيراد والتصدير")
st.markdown("---")

menu = [
    "📊 لوحة التقارير والأرباح",
    "🚛 الموردين والمشتريات",
    "⚙️ خط الغربلة وحساب الهالك",
    "📦 رصيد المخزن",
    "👥 العملاء والمبيعات",
    "💸 المصروفات والخزينة"
]
choice = st.sidebar.selectbox("اختر القسم", menu)

if choice == "🚛 الموردين والمشتريات":
    st.header("إدارة الموردين وشراء البذور الخام")
    col1, col2 = st.columns(2)
    with col1:
        supplier_name = st.text_input("اسم المورد / المزرعة")
        seed_type = st.selectbox("صنف البذور الخام", ["قمح خام", "برسيم حجازي خام", "برسيم بلدي خام", "شعير خام", "أخرى"])
        weight_kg = st.number_input("الكمية الواردة (بالكيلوجرام أو الجرام)", min_value=0.01, value=100.0)
    with col2:
        price_per_kg = st.number_input("سعر الوحدة (جنيه)", min_value=0.0)
        transport_cost = st.number_input("مصاريف النقل والتحميل (جنيه)", min_value=0.0)
        payment_type = st.radio("طريقة الدفع", ["كاش / نقدي", "آجل"])

    total_cost = (weight_kg * price_per_kg) + transport_cost
    st.info(f"💰 إجمالي تكلفة الشحنة: {total_cost:,.2f} جنيه")
    if st.button("حفظ فاتورة الشراء"):
        st.success("تم تسجيل الفاتورة وترحيل الكمية إلى مخزن الخام بنجاح!")

elif choice == "⚙️ خط الغربلة وحساب الهالك":
    st.header("⚙️ سجل تشغيل خط الغربلة وحساب التكلفة والهالك (يدعم من 50 جرام للأطنان)")
    
    col1, col2 = st.columns(2)
    with col1:
        batch_id = st.text_input("رقم التشغيلة (Batch ID)", value="B-101")
        raw_weight = st.number_input("وزن الخام المدخل (كجم/جرام)", min_value=0.01, value=1000.0)
        clean_weight = st.number_input("وزن البذور الصافية النظيفة", min_value=0.0, value=900.0)
        waste_weight = st.number_input("وزن الهالك والشوائب", min_value=0.0, value=70.0)
        sub_product_weight = st.number_input("وزن التبن / الكسر", min_value=0.0, value=30.0)

    with col2:
        raw_batch_cost = st.number_input("تكلفة دفعة الخام (جنيه)", min_value=0.0, value=15000.0)
        operating_cost = st.number_input("مصاريف الغربلة والشكائر (جنيه)", min_value=0.0, value=1000.0)
        sub_product_revenue = st.number_input("إيراد بيع التبن / الهالك (إن وجد)", min_value=0.0, value=300.0)

    waste_percentage = (waste_weight / raw_weight) * 100 if raw_weight > 0 else 0
    extraction_percentage = (clean_weight / raw_weight) * 100 if raw_weight > 0 else 0
    
    net_total_cost = raw_batch_cost + operating_cost - sub_product_revenue
    cost_per_kg = net_total_cost / clean_weight if clean_weight > 0 else 0
    cost_per_50g = cost_per_kg * 0.05  # تكلفة عبوة 50 جرام

    st.markdown("---")
    st.subheader("📊 النتائج والتكلفة الفعلية:")
    res1, res2, res3 = st.columns(3)
    res1.metric("نسبة الهالك والشوائب", f"{waste_percentage:.2f}%")
    res2.metric("نسبة الاستخراج الصافي", f"{extraction_percentage:.2f}%")
    res3.metric("تكلفة الكيلو الصافي", f"{cost_per_kg:,.2f} جنيه")

    st.success(f"💡 *واقفة عليك بكام؟* عبوة الـ 50 جرام مكلفة عليك: *{cost_per_50g:,.2f} جنيه*")

elif choice == "📦 رصيد المخزن":
    st.header("📦 رصيد المخزن اللحظي")
    inventory_data = {
        "كود الصنف": ["INV-01", "INV-02", "INV-03"],
        "الصنف": ["تقاوي قمح مغربلة", "تقاوي برسيم مغربلة", "تبن / مخلفات غربلة"],
        "النوع": ["منتج تام", "منتج تام", "هالك/فرعي"],
        "الرصيد المتاح": [8500.0, 4200.0, 1200.0],
        "متوسط تكلفة الكيلو (جنيه)": [17.25, 52.00, 1.50]
    }
    st.dataframe(pd.DataFrame(inventory_data), use_container_width=True)

elif choice == "👥 العملاء والمبيعات":
    st.header("🛒 تسجيل المبيعات وحسابات العملاء")
    col1, col2 = st.columns(2)
    with col1:
        customer_name = st.text_input("اسم العميل / التاجر")
        item_sold = st.selectbox("الصنف المباع", ["تقاوي قمح مغربلة", "تقاوي برسيم مغربلة", "عبوات 50 جرام", "تبن / كسر"])
        quantity = st.number_input("الكمية المباعة", min_value=0.01, value=1.0)
    with col2:
        unit_price = st.number_input("سعر بيع الوحدة (جنيه)", min_value=0.0)
        cost_per_unit = st.number_input("التكلفة الفعلية للوحدة", min_value=0.0, value=10.0)

    total_invoice = quantity * unit_price
    net_profit = total_invoice - (quantity * cost_per_unit)
    st.info(f"💵 إجمالي الفاتورة: {total_invoice:,.2f} جنيه | 📈 ربح الفاتورة: {net_profit:,.2f} جنيه")

elif choice == "💸 المصروفات والخزينة":
    st.header("💸 المصروفات والخزينة")
    st.selectbox("نوع المصروف", ["تشغيل مصنع", "أجور وعمالة", "مصروفات إدارية ونقل", "شكائر ومواد تعبئة"])
    st.number_input("المبلغ (جنيه)", min_value=0.0)
    st.text_area("بيان / ملاحظات")
    if st.button("تسجيل المصروف"):
        st.success("تم تسجيل المصروف بنجاح.")

elif choice == "📊 لوحة التقارير والأرباح":
    st.header("📊 لوحة التقارير والأرباح")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("إجمالي المبيعات", "145,000 جنيه")
    m2.metric("تكلفة البضاعة", "98,000 جنيه")
    m3.metric("المصروفات", "7,500 جنيه")
    m4.metric("صافي الربح الفعلي", "39,500 جنيه
