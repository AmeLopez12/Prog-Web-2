from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # Para simplicidad; en prod usa tokens
from django.views.decorators.http import require_http_methods

# Datos hardcodeados (estados y municipios de Mexico)
ESTADOS_MUNICIPIOS = {
    'Aguascalientes': ['Aguascalientes', 'Asientos', 'Calvillo', 'Cosío', 'Jesús María', 'Llano, El', 'Pabellón de Arteaga', 'Rincón de Romos', 'San Francisco de los Romo', 'San José de Gracia'],
    'Baja California': ['Ensenada', 'Mexicali', 'Playas de Rosarito', 'San Felipe', 'San Quintín', 'Tecate', 'Tijuana'],
    'Baja California Sur': ['Comondú', 'La Paz', 'Loreto', 'Los Cabos', 'Mulegé'],
    'Campeche': ['Calakmul', 'Calkiní', 'Campeche', 'Candelaria', 'Carmen', 'Champotón', 'Dzidbalché', 'Escárcega', 'Hecelchakán', 'Hopelchén'],
    'Chiapas': ['Acacoyagua', 'Acala', 'Acapetahua', 'Aldama', 'Altamirano', 'Amatán', 'Amatenango de la Frontera', 'Amatenango del Valle', 'Angel Albino Corzo', 'Arriaga'],
    'Chihuahua': ['Ahumada', 'Aldama', 'Allende', 'Aquiles Serdán', 'Ascensión', 'Bachíniva', 'Balleza', 'Batopilas de Manuel Gómez Morín', 'Bocoyna', 'Buenaventura'],
    'Ciudad de México': ['Álvaro Obregón', 'Azcapotzalco', 'Benito Juárez', 'Coyoacán', 'Cuajimalpa de Morelos', 'Cuauhtémoc', 'Gustavo A. Madero', 'Iztacalco', 'Iztapalapa', 'La Magdalena Contreras'],
    'Coahuila de Zaragoza': ['Abasolo', 'Acuña', 'Allende', 'Arteaga', 'Candela', 'Castaños', 'Cuatro Ciénegas', 'Escobedo', 'Francisco I. Madero', 'Frontera'],
    'Colima': ['Armería', 'Colima', 'Comala', 'Coquimatlán', 'Cuauhtémoc', 'Ixtlahuacán', 'Manzanillo', 'Minatitlán', 'Tecomán', 'Villa de Álvarez'],
    'Durango': ['Canatlán', 'Canelas', 'Coneto de Comonfort', 'Cuencamé', 'Durango', 'El Salto', 'General Simón Bolívar', 'Gómez Palacio', 'Guadalupe Victoria', 'Guanaceví'],
    'Guanajuato': ['Abasolo', 'Acámbaro', 'Apaseo el Alto', 'Apaseo el Grande', 'Atarjea', 'Celaya', 'Comonfort', 'Coroneo', 'Cortazar', 'Cuerámaro','Moroleon','Uriangato','Yuriria'],
    'Guerrero': ['Acapulco de Juárez', 'Ahuacuotzingo', 'Ajuchitlán del Progreso', 'Alcozauca de Guerrero', 'Alpoyeca', 'Atenango del Río', 'Atlamajalcingo del Monte', 'Atlixtac', 'Atoyac de Álvarez', 'Ayutla de los Libres'],
    'Hidalgo': ['Acatlán', 'Acaxochitlán', 'Actopan', 'Agua Blanca de Iturbide', 'Ajacuba', 'Alfajayucan', 'Almoloya', 'Apan', 'Atitalaquia', 'Atlapexco'],
    'Jalisco': ['Acatic', 'Acatlán de Juárez', 'Ahualulco de Mercado', 'Amacueca', 'Amatitán', 'Ameca', 'Arandas', 'Atemajac de Brizuela', 'Atengo', 'Atenguillo'],
    'México': ['Acambay de Ruíz Castañeda', 'Acolman', 'Aculco', 'Almoloya de Alquisiras', 'Almoloya de Juárez', 'Almoloya del Río', 'Amanalco', 'Amatepec', 'Amecameca', 'Apaxco'],
    'Michoacán de Ocampo': ['Acuitzio', 'Aguililla', 'Álvaro Obregón', 'Angamacutiro', 'Angangueo', 'Apatzingán', 'Aporo', 'Aquila', 'Ario', 'Arteaga'],
    'Morelos': ['Amacuzac', 'Atlatlahucan', 'Axochiapan', 'Ayala', 'Coatlán del Río', 'Cuautla', 'Cuernavaca', 'Emiliano Zapata', 'Huitzilac', 'Jantetelco'],
    'Nayarit': ['Acaponeta', 'Ahuacatlán', 'Amatlán de Cañas', 'Bahía de Banderas', 'Compostela', 'Huajicori', 'Ixtlán del Río', 'Jala', 'Xalisco', 'Del Nayar'],
    'Nuevo León': ['Abasolo', 'Agualeguas', 'Allende', 'Anáhuac', 'Apodaca', 'Aramberri', 'Bustamante', 'Cadereyta Jiménez', 'Cerralvo', 'China'],
    'Oaxaca': ['Abejones', 'Acatepec', 'Asunción Cacalotepec', 'Asunción Cuyotepec', 'Asunción Ixtaltepec', 'Asunción Ocotlán', 'Asunción Tlacolulita', 'Ayotzintepec', 'El Barrio de la Soledad', 'Calihualá'],
    'Puebla': ['Acajete', 'Acateno', 'Acatlán', 'Acatzingo', 'Acteopan', 'Ahuacatlán', 'Ahuatlán', 'Ahuazotepec', 'Ahuehuetitla', 'Ajalpan'],
    'Querétaro': ['Amealco de Bonfil', 'Arroyo Seco', 'Cadereyta de Montes', 'Colón', 'Corregidora', 'Ezequiel Montes', 'Huimilpan', 'Jalpan de Serra', 'Landa de Matamoros', 'El Marqués'],
    'Quintana Roo': ['Bacalar', 'Benito Juárez', 'Cozumel', 'Felipe Carrillo Puerto', 'Isla Mujeres', 'José María Morelos', 'Lázaro Cárdenas', 'Othón P. Blanco', 'Puerto Morelos', 'Solidaridad'],
    'San Luis Potosí': ['Ahualulco', 'Alaquines', 'Aquismón', 'Armadillo de los Infante', 'Cárdenas', 'Catorce', 'Cedral', 'Cerritos', 'Cerro de San Pedro', 'Ciudad del Maíz'],
    'Sinaloa': ['Ahome', 'Angostura', 'Badiraguato', 'Choix', 'Concordia', 'Cosalá', 'Culiacán', 'El Fuerte', 'Elota', 'Escuinapa'],
    'Sonora': ['Aconchi', 'Agua Prieta', 'Alamos', 'Altar', 'Arivechi', 'Arizpe', 'Atil', 'Bacadéhuachi', 'Bacanora', 'Bacerac'],
    'Tabasco': ['Balancán', 'Cárdenas', 'Centla', 'Centro', 'Comalcalco', 'Cunduacán', 'Emiliano Zapata', 'Huimanguillo', 'Jalapa', 'Jalpa de Méndez'],
    'Tamaulipas': ['Abasolo', 'Aldama', 'Altamira', 'Antiguo Morelos', 'Burgos', 'Bustamante', 'Camargo', 'Casas', 'Ciudad Madero', 'Cruillas'],
    'Tlaxcala': ['Acuamanala de Miguel Hidalgo', 'Amaxac de Guerrero', 'Apetatitlán de Antonio Carvajal', 'Apizaco', 'Atlangatepec', 'Atltzayanca', 'Benito Juárez', 'Calpulalpan', 'Contla de Juan Cuamatzi', 'Cuapiaxtla'],
    'Veracruz de Ignacio de la Llave': ['Acajete', 'Acatlán', 'Acayucan', 'Actopan', 'Acula', 'Acultzingo', 'Adalberto Tejeda', 'Agua Dulce', 'Álamo Temapache', 'Alpatláhuac'],
    'Yucatán': ['Abalá', 'Acanceh', 'Akil', 'Baca', 'Cacalchén', 'Calotmul', 'Cansahcab', 'Cantamayec', 'Celestún', 'Cenotillo'],
    'Zacatecas': ['Apozol', 'Atolinga', 'Benito Juárez', 'Calera', 'Cañitas de Felipe Pescador', 'Concepción del Oro', 'Cuauhtémoc', 'Chalchihuites', 'El Plateado de Joaquín Amaro', 'El Salvador']
}

@require_http_methods(["GET"])
def index(request):
    estados = list(ESTADOS_MUNICIPIOS.keys())
    return render(request, 'lugares/index.html', {'estados': estados})

@require_http_methods(["GET"])
def get_municipios(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        estado = request.GET.get('estado')
        if estado in ESTADOS_MUNICIPIOS:
            municipios = ESTADOS_MUNICIPIOS[estado]
            return JsonResponse({'municipios': municipios})
        return JsonResponse({'error': 'Estado no encontrado'}, status=400)
    return JsonResponse({'error': 'Solicitud inválida'}, status=400)