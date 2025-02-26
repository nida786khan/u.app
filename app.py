import streamlit as st
import pint
import re

# Streamlit App Title
st.title("🌍 Ultimate Unit Converter 🔥")

# Initialize unit registry
ureg = pint.UnitRegistry()

# Unit Categories
unit_categories = {
    "Length": ["nanometer", "nm", "millimeter", "mm", "centimeter", "cm", "meter", "kilometer", "mile", "yard", "foot", "inch"],
    "Weight": ["gram", "kilogram", "ton", "pound", "ounce"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
    "Time": ["second", "minute", "hour", "day"],
    "Area": ["square meter", "square kilometer", "square mile", "acre"],
    "Speed": ["m/s", "km/h", "mph", "knot"],
    "Volume": ["liter", "litre", "millilitre", "gallon", "cubic meter", "fluid ounce", "fl oz"],
    "Energy": ["joule", "calorie", "watt-hour"],
    "Pressure": ["pascal", "bar", "psi"],
    "Power": ["watt", "kilowatt", "horsepower"]
}

# Sidebar Navigation
st.sidebar.title("🌟 Navigation")
selected_menu = st.sidebar.radio("Select Menu", ("Manual Converter", "AI Chatbot"))

def convert_units(quantity, from_unit, to_unit):
    try:
        converted_value = (quantity * ureg(from_unit)).to(to_unit)
        return converted_value
    except pint.errors.UndefinedUnitError:
        return "⚠️ One or both units are invalid! Check spelling and format."
    except pint.errors.DimensionalityError:
        return "⚠️ Units are not from the same category!"
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def get_unit_category(unit):
    unit = unit.lower()
    for category, units in unit_categories.items():
        if unit in [u.lower() for u in units]:
            return category
    return None

def normalize_unit(unit):
    unit = unit.lower().strip()
    unit_aliases = {
        "km": "kilometer", "miles": "mile", "mi": "mile",
        "feet": "foot", "ft": "foot", "inch": "inch", "in": "inch",
        "litres": "liter", "liters": "liter", "ml": "millilitre",
        "fl oz": "fluid ounce", "oz": "ounce", "kg": "kilogram",
        "g": "gram", "lbs": "pound", "lb": "pound"
    }
    return unit_aliases.get(unit, unit)

# 📌 Manual Unit Converter
if selected_menu == "Manual Converter":
    st.header("🔄 Effortless Unit Converter")
    st.markdown("### Convert units seamlessly across multiple categories.")
    
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("📂 Select Category", list(unit_categories.keys()))
    with col2:
        quantity = st.number_input("🔢 Enter Value", min_value=0.0, format="%.6f")

    col3, col4 = st.columns(2)
    with col3:
        from_unit = st.selectbox("🔄 From Unit", unit_categories[category])
    with col4:
        to_unit = st.selectbox("➡️ To Unit", unit_categories[category])

    if st.button("🚀 Convert Now"):
        result = convert_units(quantity, from_unit, to_unit)
        if isinstance(result, pint.Quantity):
            st.success(f"✅ {quantity} {from_unit} = {result:.6f} {to_unit}")
        else:
            st.error(result)

# 📌 AI Chatbot for Conversion
if selected_menu == "AI Chatbot":
    st.header("🤖 Intelligent Unit Conversion Assistant")

    def rule_based_chatbot(query):
        query = query.lower()
        pattern = r"convert\s*([0-9]+(?:\.[0-9]+)?)\s*([a-zA-Z ]+)\s*(?:to|in)\s*([a-zA-Z ]+)"
        match = re.search(pattern, query)

        if match:
            number = float(match.group(1))
            from_u = normalize_unit(match.group(2))
            to_u = normalize_unit(match.group(3))

            from_category = get_unit_category(from_u)
            to_category = get_unit_category(to_u)

            if not from_category or not to_category:
                return "⚠️ One or both units are invalid! Did you mean something else?"

            if from_category != to_category:
                return "⚠️ Units are not from the same category! Try again."

            result = convert_units(number, from_u, to_u)
            if isinstance(result, pint.Quantity):
                return f"✅ {number} {from_u} = {result:.6f} {to_u}"
            return result

        return "❌ Invalid format! Please use: Convert 10 km to miles."

    query = st.text_input("💬 Ask AI: (e.g., Convert 10 km to miles)")
    if st.button("🤔 Ask AI"):
        if query:
            answer = rule_based_chatbot(query)
            st.write("🤖 AI Says:", answer)
        else:
            st.warning("⚠️ Please enter a query!")

















