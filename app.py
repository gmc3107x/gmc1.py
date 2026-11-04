import re
import streamlit as st

# Configuración de la página para dispositivos móviles
st.set_page_config(
    page_title="Extractor Pago Móvil",
    page_icon="💸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS personalizados para que luzca limpio, moderno y tipo app móvil
st.markdown("""
    <style>
    .main {
        background-color: #e3f2fd;
    }
    .stButton>button {
        width: 100%;
        background-color: #1976d2;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem;
    }
    .stButton>button:hover {
        background-color: #115293;
        color: white;
    }
    h1 {
        color: #0d47a1;
        text-align: center;
        font-size: 1.5rem !important;
    }
    </style>
""", unsafe_allow_html=True)

def extraer_datos_pago(texto):
    telefono = ""
    cedula = ""
    monto = ""

    # 1. Extraer teléfono (11 dígitos exactos)
    patron_tel = r'(0(?:412|414|422|424|416|426|212|241|251|261|271|281|291)\d{7})'
    match_tel = re.search(patron_tel, texto)
    if match_tel:
        telefono = match_tel.group(1).strip()
        texto_trabajo = texto.replace(telefono, " ")
    else:
        texto_trabajo = texto

    # 2. Extraer cédula (6 a 8 dígitos)
    posibles_cedulas = re.findall(r'\b\d{6,8}\b', texto_trabajo)
    if posibles_cedulas:
        cedula = posibles_cedulas[0]
        texto_trabajo = texto_trabajo.replace(cedula, " ")

    # 3. Extraer monto
    matches_montos = re.findall(r'\b\d+\b', texto_trabajo)
    if matches_montos:
        montos_limpios = [m for m in matches_montos if m.strip()]
        if montos_limpios:
            monto = montos_limpios[-1]

    # 4. Búsqueda de bancos
    bancos_claves = {
        "Banco Venezolano De Crédito": ["venezolano de credito", "venezolano de crédito"],
        "Banco De Venezuela": ["banco de venezuela", " bdv ", " venezuela"],
        "Banesco": ["banesco"],
        "Banco Mercantil": ["mercantil"],
        "Banco Provincial": ["provincial", "bbva provincial"],
        "Bancaribe": ["bancaribe"],
        "Banco Nacional De Crédito": ["nacional de credito", "nacional de crédito", " bnc "],
        "Bancamiga": ["bancamiga"],
        "Banplus": ["banplus"],
        "Fondo Común": ["fondo comun", "fondo común", " bfc "],
        "Banco Exterior": ["banco exterior", " exterior "],
        "Banco Del Tesoro": ["banco del tesoro", " del tesoro "],
        "Banco Bicentenario": ["bicentenario"],
        "Sofitasa": ["sofitasa"],
        "Banco Activo": ["banco activo", " activo "],
        "Bancrecer": ["bancrecer"],
        "Banco Plaza": ["banco plaza", " plaza "],
        "Banco Caroní": ["caroni", "caroní"],
        "100% Banco": ["100% banco", "100 por ciento banco"],
        "Mi Banco": ["mi banco"],
        "Banco Agrícola": ["agricola", "agrícola"]
    }
    
    banco_encontrado = ""
    texto_lower = texto.lower()
    for banco_formal, palabras_clave in bancos_claves.items():
        for clave in palabras_clave:
            if clave in texto_lower:
                banco_encontrado = banco_formal
                break
        if banco_encontrado:
            break

    return banco_encontrado, telefono, cedula, monto

# --- INTERFAZ WEB ---
st.markdown("<h1>Extractor Pago Móvil GMC</h1>", unsafe_allow_html=True)
st.write("Pega el texto del mensaje de pago abajo:")

# Área de texto para pegar el mensaje completo
texto_ingresado = st.text_area("", placeholder="Ej: Acredito PagoMovil Banesco 04141234567 25123456 1500.00...", height=100)

lista_bancos_venezuela = [
    "Seleccione o escriba el banco...",
    "Banco de Venezuela", "Banesco", "Banco Mercantil", "Banco Provincial",
    "Bancaribe", "Banco Nacional de Crédito", "Bancamiga", "Banplus",
    "Fondo Común", "Banco Exterior", "Banco del Tesoro", "Banco Bicentenario",
    "Sofitasa", "Banco Activo", "Bancrecer", "Banco Plaza", "Banco Caroní",
    "100% Banco", "Mi Banco", "Banco Agrícola"
]

if st.button("Separar Datos"):
    if texto_ingresado.strip():
        banco, telefono, cedula, monto = extraer_datos_pago(texto_ingresado)
        
        # Guardar en el estado de sesión para mantener los datos en pantalla
        st.session_state['banco'] = banco if banco else "Seleccione o escriba el banco..."
        st.session_state['telefono'] = telefono
        st.session_state['cedula'] = cedula
        st.session_state['monto'] = monto
    else:
        st.warning("Por favor ingresa un texto primero.")

# Recuperar valores si ya fueron procesados
banco_val = st.session_state.get('banco', "Seleccione o escriba el banco...")
tel_val = st.session_state.get('telefono', "")
ced_val = st.session_state.get('cedula', "")
monto_val = st.session_state.get('monto', "")

st.markdown("---")

# Resultados con campos limpios
try:
    idx_banco = lista_bancos_venezuela.index(banco_val)
except ValueError:
    idx_banco = 0

banco_seleccionado = st.selectbox("Banco:", lista_bancos_venezuela, index=idx_banco)
tel_input = st.text_input("Teléfono:", value=tel_val)
ced_input = st.text_input("Cédula:", value=ced_val)
monto_input = st.text_input("Monto:", value=monto_val)