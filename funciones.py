
from fpdf import FPDF
import os

def check_parada(cur,parada):
    cur.execute(f"SELECT autorizar FROM tabla_index WHERE nombre = '{parada}' ")
    check=cur.fetchall()
    for valor in check:
        if valor[0] == 'autorizada':
            return True
        else: 
            return False
    
def listado_paradas(cur):
    cur.execute("SELECT nombre FROM tabla_index")  
    db_paradas=cur.fetchall()     
    return db_paradas

def info_parada(cur,parada):
    cur.execute(f"SELECT codigo,nombre,direccion,municipio,provincia,zona,cuota,pago,banco,num_cuenta,federacion,geolocalizacion FROM  tabla_index  WHERE nombre='{parada}'" )
    infos=cur.fetchall()     
    return infos

def info_cabecera(cur,parada):          
    cur.execute(f'SELECT nombre FROM {parada}')
    seleccion=cur.fetchall()
    cant=len(seleccion)  
    presidente = []
    ced_presidente=[]       
    cur.execute(f"SELECT nombre,cedula FROM {parada}  WHERE funcion = 'Presidente'")   
    press=cur.fetchall()
    if press != []:  
     for pres in press:   
        presidente=pres[0]
        ced_presidente=pres[1]
    else:     
       presidente='No disponible'            
    return cant,presidente,ced_presidente                
     
def lista_miembros(cur,parada):
    listas=[]
    cur.execute(f"SELECT id,nombre,cedula,telefono,funcion  FROM {parada}")
    miembros=cur.fetchall()
    for miembro in miembros:     
        listas+=miembro    
    lista=dividir_lista(listas,5)    
    return lista
    
def diario_general(cur,parada):
    prestamos=[]
    ingresos=[]
    gastos=[]
    aporte=[]
    pendiente=[]
    abonos=[]
    balance_bancario=[]
    cur.execute(f"SELECT  prestamos, ingresos, gastos, aporte, pendiente, abonos, balance_banco FROM tabla_index WHERE nombre='{parada}' " )  
    consult=cur.fetchall()
    for valor in consult:
        prestamos=valor[0]
        ingresos=valor[1]
        gastos=valor[2]
        aporte=valor[3]
        pendiente=valor[4]
        abonos=valor[5]
        balance_bancario=valor[6]
    balance=(aporte + ingresos + abonos )-(gastos+prestamos)
    data=(balance,prestamos,ingresos,gastos,aporte,pendiente,abonos,balance_bancario)   
    return data

def pendiente_aport(cur,parada):
    var1=[]
    var2=[]
    cur.execute(f"SHOW TABLES LIKE '{parada}_cuota'")
    vericar=cur.fetchall()
    if vericar !=[]:
      vgral=[]
      cur.execute(f"SELECT nombre FROM {parada}")
      list_nomb=cur.fetchall()
      for nombre in list_nomb:
         cur.execute(f"SELECT COUNT(estado) FROM {parada}_cuota WHERE estado = 'pago' and nombre='{nombre[0]}'") 
         var_x = cur.fetchall()
         for var_p in var_x:
              var1=var_p[0]
         cur.execute(f"SELECT COUNT(estado) FROM {parada}_cuota WHERE estado = 'no_pago' and nombre='{nombre[0]}'")
         var_z = cur.fetchall()
         for var_n in var_z:
              var2=var_n[0]   
         sub_t=var1+var2
         if sub_t != 0 :    
          avg=round((var1/sub_t)*100,2)
         else:
          avg = 0.00               
         vgral+=(nombre[0],var1,var2,sub_t,avg) 
      list_1=dividir_lista(vgral,5)                    
      return list_1
    else:
      return [] 




def lista_prestamos(cur,parada):
    cur.execute(f"SHOW TABLES LIKE '{parada}_prestamos'")
    verificar=cur.fetchall()
    if verificar !=[]:
      cur.execute(f"SELECT prestamo_a FROM {parada}_prestamos")
      nombres=cur.fetchall()
      return nombres
    return []



def dividir_lista(lista,lon) : 
    return [lista[n:n+lon] for n in range(0,len(lista),lon)]     


def aportacion(cur,parada):           
    cur.execute(f"SELECT codigo, nombre, cedula, telefono, funcion FROM {parada}")
    data=cur.fetchall()
    return data
  
def verif_p(cur,parada,cedula):
    cur.execute(f"SELECT * FROM {parada} WHERE  cedula = '{cedula}'")                                       
    accounts =cur.fetchall()
    if accounts != []:
         return True
    else:
         return False 
     
def nombres_miembro(cur,parada):
        listado=[]
        cur.execute(f"SELECT nombre FROM {parada} ")
        nombres=cur.fetchall()
        for nombre in nombres:
            listado += nombre
        return listado 
    
def info_personal(cur,parada,cedula):
    if parada !=[] and cedula !=[] :
      nombre = []
      cur.execute(f"SELECT nombre FROM {parada} WHERE cedula='{cedula}'")   
      nombres=cur.fetchall()
      for nombre in nombres: 
       return nombre[0]
    else:
      return []  

def verificar_prestamo(cur,parada,cedula):
    
    cur.execute(f"SHOW TABLES LIKE '{parada}_prestamos'")
    vericar=cur.fetchall()
    if vericar !=[]:    
        prestado=[]    
        nombre=[]
        cur.execute(f"SELECT nombre FROM {parada} WHERE cedula = '{cedula}'") 
        nombres = cur.fetchall()
        for pers in nombres:
            nombre=pers[0]
        cur.execute(f"SELECT fecha,monto_prestamo FROM {parada}_prestamos WHERE prestamo_a ='{nombre}'") 
        prestamo=cur.fetchall()
        if prestamo !=[]:
           for prestado in prestamo:   
             return (f"usted tomo un prestamo en fecha {prestado[0]},por un monto de {prestado[1]}RD$") 
        else:
           return 'No tiene prestamo a este momento'
    else:
        return 'No hay registro de prestamo ene esta parada'


def verificar_abonos(cur,parada,cedula,prestamo):
    if (str(prestamo) != 'No tiene prestamo a este momento' ) or (str(prestamo) !='No hay registro de prestamo en esta parada'):
        
       return  'Tiene abonos pendientes de su deuda'
    else:
        return 'No teneno deuda registrada de usted en nuestros archivo'
    
    
def hist_pago(cur,parada,nombre): 
    var1=[] 
    var2=[] 
    cur.execute(f"SHOW TABLES LIKE '{parada}_cuota'")
    vericar=cur.fetchall()
    if vericar !=[]:    
         cur.execute(f"SELECT COUNT(estado) FROM {parada}_cuota WHERE estado = 'pago' and nombre='{nombre}'") 
         var_x = cur.fetchall()
         for var_p in var_x:
              var1=var_p[0]
         cur.execute(f"SELECT COUNT(estado) FROM {parada}_cuota WHERE estado = 'no_pago' and nombre='{nombre}'")
         var_z = cur.fetchall()
         for var_n in var_z:
              var2=var_n[0]   
         sub_t=var1+var2
         if sub_t != 0 :    
          avg=round((var1/sub_t)*100,2)
         else:
            avg = 0.00                                           
         return (f" {sub_t} cuotas usted a pagado {var1} cuotas y tiene pendiente de pagar {var2} cuotas  por tanto su promedio de pago es de { avg}%",avg) 
    else:
      return ' de 0 cuotas no hay cuotas en atraso',0  
    
def visibilidad(pagos):
    if float(pagos) > 49 :
      return 'ver'   
    else:
        return 'no_ver'
    
def dat_miembros(cur,parada,miembro):
    cur.execute(f"SELECT nombre,cedula,telefono,funcion FROM {parada} WHERE nombre='{miembro}'")
    listado=cur.fetchall()
    return listado

def vef_cedula(cur,cedula):
  lista_paradas=[]  
  cur.execute("SELECT nombre FROM tabla_index")  
  db_paradas=cur.fetchall()    
  for parada in db_paradas:
      lista_paradas+=parada   
  for parada in lista_paradas:
      cur.execute(f"SELECT nombre FROM {parada} WHERE cedula='{cedula}'")
      nombre=cur.fetchall()
      if nombre !=[]:            
        return parada             
  return []    

def crear_pago(cur,parada,string,valor_cuota,hoy):
       suma_no=[];suma_si=[]
       cur.execute(f'CREATE TABLE IF NOT EXISTS {parada}_cuota( item VARCHAR(50)  NULL, fecha VARCHAR(50)  NULL, estado VARCHAR(50)  NULL, nombre VARCHAR(50)  NULL, cedula VARCHAR(50)  NULL)')
       for data in string:
          cur.execute(f"INSERT INTO {parada}_cuota(item, fecha, estado, nombre, cedula) VALUES('{data[0]}', '{hoy}',  '{data[1]}', '{data[2]}', '{data[3]}')")    
       cur.execute(f"SELECT COUNT(estado) FROM {parada}_cuota WHERE estado = 'no_pago' ")   
       suma=cur.fetchall()
       for num in suma:
           suma_no=num[0]       
       cur.execute(f"SELECT COUNT(estado) FROM {parada}_cuota WHERE estado = 'pago' ")   
       sumas=cur.fetchall() 
       for numb in sumas:
           suma_si=numb[0]        
       n_aporte=int(suma_si) * float(valor_cuota)
       n_pendiente=int(suma_no) * float(valor_cuota)
       cur.execute(f"UPDATE tabla_index SET aporte={n_aporte}, pendiente={n_pendiente} WHERE nombre='{parada}'")
       return

def estado_bancario(cur,parada,fecha,banco,cuenta,operacion,monto,balance) : 
    cur.execute(f"CREATE TABLE IF NOT EXISTS {parada}_banco( id int NOT NULL AUTO_INCREMENT ,fecha VARCHAR(50)  NULL, banco VARCHAR(50) NULL, operacion VARCHAR(50) NULL,  numero_cuenta VARCHAR(50) NULL, monto DECIMAl(10,2) unsigned DEFAULT 0, balance DECIMAl(10,2) unsigned DEFAULT 0,PRIMARY KEY(id))")                                                                                                                                
    cur.execute(f"INSERT INTO {parada}_banco(fecha, banco, numero_cuenta, operacion, monto, balance) VALUES('{fecha}', '{banco}', '{cuenta}', '{operacion}',{monto},{balance})")
    return  

def report_gastos(cur,parada,fecha,descripcion_gastos,cantidad_gastos):
     n_gastos=[] 
     cur.execute(f"CREATE TABLE IF NOT EXISTS {parada}_gastos( id int NOT NULL AUTO_INCREMENT ,fecha VARCHAR(50)  NULL,descripcion_gastos VARCHAR(50) NULL, cantidad_gastos DECIMAl(10,2) unsigned DEFAULT 0, PRIMARY KEY(id))")                                                                                                                         
     cur.execute(f"INSERT INTO {parada}_gastos(fecha, descripcion_gastos, cantidad_gastos) VALUES('{fecha}', '{descripcion_gastos}', {cantidad_gastos})")
     cur.execute(f"SELECT SUM(cantidad_gastos) FROM  {parada}_gastos ")
     suma=cur.fetchall() 
     for total in suma:
        n_gastos=total[0]   
     cur.execute(f"UPDATE tabla_index SET gastos={n_gastos} WHERE nombre='{parada}'")
     return
 
def report_ingresos(cur,parada,fecha,descripcion_ingreso,cantidad_ingreso):
       n_ingresos=[]    
       cur.execute(f"CREATE TABLE IF NOT EXISTS {parada}_ingresos( id int NOT NULL AUTO_INCREMENT ,fecha VARCHAR(50)  NULL, descripcion_ingresos VARCHAR(50)  NULL, cantidad_ingresos DECIMAl(10,2) unsigned DEFAULT 0 , PRIMARY KEY(id))" )                                                                                                                               
       cur.execute(f"INSERT INTO {parada}_ingresos(fecha, descripcion_ingresos, cantidad_ingresos) VALUES('{fecha}', '{descripcion_ingreso}', { cantidad_ingreso})")       
       cur.execute(f"SELECT SUM(cantidad_ingresos) FROM  {parada}_ingresos ")
       suma=cur.fetchall()
       for total in suma:  
         n_ingresos=total[0]       
       cur.execute(f"UPDATE tabla_index SET ingresos={n_ingresos}  WHERE nombre='{parada}'")
       return
 
def report_prestamo(cur,parada,fecha,prestamo,monto): 
       n_prestamos=[]     
       cur.execute(f"CREATE TABLE IF NOT EXISTS {parada}_prestamos( id int NOT NULL AUTO_INCREMENT ,fecha VARCHAR(50)  NULL, prestamo_a VARCHAR(50)  NULL, monto_prestamo DECIMAl(10,2) unsigned DEFAULT 0, PRIMARY KEY(id) )")                                                                                                                                 
       cur.execute(f"INSERT INTO {parada}_prestamos(fecha, prestamo_a, monto_prestamo) VALUES('{fecha}',  '{prestamo}', {monto})")            
       cur.execute(f"SELECT SUM(monto_prestamo)  FROM  {parada}_prestamos ")
       suma=cur.fetchone()
       for n_prestamos in suma:
         n_prestamos        
       cur.execute(f"UPDATE tabla_index SET prestamos={n_prestamos}  WHERE nombre='{parada}'")
       return     
       
def report_abono(cur,parada,fecha,abono_a,cantidad_a):
    balance_prestamos=[]
    n_abonos=[]
    prestamo=[] 
    abono_persona=[]
    cur.execute(f"CREATE TABLE IF NOT EXISTS {parada}_abonos( id int NOT NULL AUTO_INCREMENT ,fecha VARCHAR(50)  NULL,  abono_a VARCHAR(50)  NULL, monto_abono DECIMAl(10,2) unsigned DEFAULT 0, balance_prestamo DECIMAl(10,2) unsigned DEFAULT 0 , PRIMARY KEY(id))" )                                                                                                                            
    cur.execute(f"INSERT INTO {parada}_abonos(fecha, abono_a, monto_abono) VALUES('{fecha}', '{abono_a}', {cantidad_a})")         
    cur.execute(f"SELECT SUM(monto_abono) FROM  {parada} ")
    suma=cur.fetchone() 
    for n_abonos in suma: 
       n_abonos  
    cur.execute(f"SELECT SUM(monto_abono) FROM  {parada}_abonos WHERE abono_a='{abono_a}' ")
    suma=cur.fetchone() 
    for abono_persona in suma: 
        abono_persona
    cur.execute(f"SELECT monto_prestamo FROM  {parada}_prestamos WHERE prestamo_a = '{abono_a}' ")
    prestado=cur.fetchone()
    for prestamo in prestado:
        prestamo          
    if prestamo==[] or prestamo== 0:
      cur.execute(f"UPDATE {parada} SET balance_prestamo = 0.0 ")
      return
    else:       
      return 
  
def imprimir(cur,parada,fecha,descripcion,cantidad,titulo,president,miembros,item):
    infor=info_parada(cur,parada)
    for datos in infor:
        pdf = FPDF()
        pdf = FPDF(orientation='P',unit='mm',format='Letter')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('arial', '', 13.0)
        pdf.set_xy(50.0, 8.0)
        pdf.cell(ln=0, h=22.0, align='C', w=75.0, txt=f'{titulo}', border=0)
        pdf.set_line_width(0.0)
        pdf.rect(15.0, 15.0, 170.0, 100.0)
        pdf.image('C:/Users/juanc/Desktop/proyecto motoben-actec/actec-bootrap/static/imagenes/logo-motoben.jpg', 20.0, 17.0, link='', type='', w=30.0, h=30.0)
        pdf.set_font('arial', '', 8.0)
        pdf.set_xy(50.0, 21.0)
        pdf.cell(ln=0, h=4.0, align='C', w=75.0, txt='Original', border=0)
        pdf.set_font('arial', 'B', 12.0) 
        pdf.set_xy(115.0, 25.0)
        pdf.cell(ln=0, h=7.0, align='L', w=60.0, txt='Fecha:', border=0)
        pdf.set_xy(135.0, 25.0)
        pdf.cell(ln=0, h=7.0, align='L', w=40.0, txt=f'{fecha}', border=0)
        pdf.set_font('arial', 'B', 14.0)
        pdf.set_xy(115.0, 31.0)
        pdf.cell(ln=0, h=5.5, align='L', w=10.0, txt='N\xba: ', border=0)
        pdf.set_xy(135.0, 31.0)
        pdf.cell(ln=0, h=9.5, align='L', w=60.0, txt='00000001', border=0)
        pdf.set_font('arial', 'B', 12.0)
        pdf.set_xy(18.0, 48)
        pdf.cell(ln=0, h=5.0, align='L', w=98.0, txt='GRUPO ACTEC', border=0)    
        pdf.set_font('arial', '', 8.0)
        pdf.set_xy(0.0, 53.0)
        pdf.cell(ln=0, h=4.0, align='C', w=75.0, txt='Tecnologia 4.0', border=0)
        pdf.set_font('arial', '', 12.0)        
        pdf.set_line_width(0.0)
        pdf.line(15.0, 57.0, 185.0, 57.0)
        pdf.set_font('arial', 'B', 10.0)
        pdf.set_xy(17.0, 59.0)
        pdf.cell(ln=0, h=6.0, align='L', w=13.0, txt='PARADA:', border=0)
        pdf.set_xy(45.0, 59.0)
        pdf.cell(ln=0, h=6.0, align='L', w=140.0, txt=f'{datos[1]}', border=0)
        pdf.set_xy(17.0, 64.0)
        pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='PRESIDENTE:', border=0)
        pdf.set_xy(45.0, 64.0)
        pdf.cell(ln=0, h=6.0, align='L', w=125.0, txt=f'{president}', border=0)
        pdf.set_xy(17.0, 69.0)
        pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='MUNICIPIO:', border=0)
        pdf.set_xy(45.0, 69.0)
        pdf.cell(ln=0, h=6.0, align='L', w=80.0, txt=f'{datos[3]}', border=0)
        pdf.set_xy(17.0, 74.0)
        pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='DIRECCION:', border=0)
        pdf.set_xy(45.0, 74.0)
        pdf.cell(ln=0, h=6.0, align='L', w=42.0, txt=f'{datos[2]}', border=0)    
        pdf.set_xy(17.0, 80.0)
        pdf.cell(ln=0, h=5.0, align='L', w=15.0, txt='Provincia:', border=0)
        pdf.set_xy(45.0, 80.0)
        pdf.cell(ln=0, h=5.0, align='L', w=70.0, txt=f'{datos[4]}', border=0)
        pdf.set_xy(115.0, 80.0)
        pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt='CODIGO:', border=0)
        pdf.set_xy(135.0, 80.0)
        pdf.cell(ln=0, h=5.0, align='L', w=40.0, txt=f'{datos[0]}', border=0)
        pdf.set_line_width(0.0)
        pdf.line(15.0, 88.0, 185.0, 88.0)
        pdf.set_xy(17.0, 90.0)
        pdf.cell(ln=0, h=5.0, align='L', w=48.0, txt='Numero de miembros:', border=0)
        pdf.set_xy(65.0, 90.0)
        pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt=f'{miembros}', border=0)
        pdf.set_xy(92.0, 90.0)
        pdf.cell(ln=0, h=5.0, align='L', w=43.0, txt='Per\xedodo Facturado', border=0)
        pdf.set_xy(125.0, 90.0)
        pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt=f'{fecha}', border=0)
        pdf.set_xy(150.0, 90.0)
        pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt='', border=0)
        pdf.set_line_width(0.0)
        pdf.line(15.0, 95.0, 185.0, 95.0)
        pdf.set_line_width(0.0)
        pdf.line(155.0, 95.0, 155.0, 100.0)
        pdf.set_xy(15.0,95.0)
        pdf.cell(w=140.0, h=10.0, txt='DESCRIPCION',border=1,ln=0,align='C',fill=0)
        pdf.multi_cell(w=30.0, h=10.0, txt='TOTAL',border=1,align='C',fill=0) 
        pdf.set_x(15)  
        pdf.cell(w=20.0, h=10.0, txt=f'{item}',border=0,ln=0,align='C',fill=0)             
        pdf.cell(w=120.0, h=10.0,txt=f'{descripcion}',border=0,ln=0,align='L',fill=0)
        pdf.multi_cell(w=30.0, h=10.0,txt=f'{cantidad}',border=0,align='C',fill=0)            
        pdf.ln(5) 
       
        pdf.output(f"C:/Users/juanc/Desktop/proyecto motoben-actec/actec-bootrap/static/pdf/factura_{parada}{titulo}{fecha}.pdf", 'F')    
        return  str(f"/static/pdf/factura_{parada}{titulo}{fecha}.pdf")
    


def imprimir_lista(cur,parada,fecha,string,valor_cuota,titulo,president,cant,cuotas):
    infor=info_parada(cur,parada)
    for datos in infor:
        pdf = FPDF()
        pdf = FPDF(orientation='P',unit='mm',format='Letter')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('arial', '', 13.0)
        pdf.set_xy(50.0, 8.0)
        pdf.cell(ln=0, h=22.0, align='C', w=75.0, txt=f'{titulo}', border=0)
        pdf.set_line_width(0.0)
        pdf.rect(15.0, 15.0, 170.0, 245.0)
        pdf.image('C:/Users/juanc/Desktop/proyecto motoben-actec/actec-bootrap/static/imagenes/logo-motoben.jpg', 20.0, 17.0, link='', type='', w=30.0, h=30.0)
        pdf.set_font('arial', '', 8.0)
        pdf.set_xy(50.0, 21.0)
        pdf.cell(ln=0, h=4.0, align='C', w=75.0, txt='Original', border=0)
        pdf.set_font('arial', 'B', 12.0) 
        pdf.set_xy(115.0, 25.0)
        pdf.cell(ln=0, h=7.0, align='L', w=60.0, txt='Fecha:', border=0)
        pdf.set_xy(135.0, 25.0)
        pdf.cell(ln=0, h=7.0, align='L', w=40.0, txt=f'{fecha}', border=0)
        pdf.set_font('arial', 'B', 14.0)
        pdf.set_xy(115.0, 31.0)
        pdf.cell(ln=0, h=5.5, align='L', w=10.0, txt='N\xba: ', border=0)
        pdf.set_xy(135.0, 31.0)
        pdf.cell(ln=0, h=9.5, align='L', w=60.0, txt='00000001', border=0)
        pdf.set_font('arial', 'B', 12.0)
        pdf.set_xy(18.0, 48)
        pdf.cell(ln=0, h=5.0, align='L', w=98.0, txt='GRUPO ACTEC', border=0)    
        pdf.set_font('arial', '', 8.0)
        pdf.set_xy(0.0, 53.0)
        pdf.cell(ln=0, h=4.0, align='C', w=75.0, txt='Tecnologia 4.0', border=0)
        pdf.set_font('arial', '', 12.0)        
        pdf.set_line_width(0.0)
        pdf.line(15.0, 57.0, 185.0, 57.0)
        pdf.set_font('arial', 'B', 10.0)
        pdf.set_xy(17.0, 59.0)
        pdf.cell(ln=0, h=6.0, align='L', w=13.0, txt='PARADA:', border=0)
        pdf.set_xy(45.0, 59.0)
        pdf.cell(ln=0, h=6.0, align='L', w=140.0, txt=f'{datos[1]}', border=0)
        pdf.set_xy(17.0, 64.0)
        pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='PRESIDENTE:', border=0)
        pdf.set_xy(45.0, 64.0)
        pdf.cell(ln=0, h=6.0, align='L', w=125.0, txt=f'{president}', border=0)
        pdf.set_xy(17.0, 69.0)
        pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='MUNICIPIO:', border=0)
        pdf.set_xy(45.0, 69.0)
        pdf.cell(ln=0, h=6.0, align='L', w=80.0, txt=f'{datos[3]}', border=0)
        pdf.set_xy(17.0, 74.0)
        pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='DIRECCION:', border=0)
        pdf.set_xy(45.0, 74.0)
        pdf.cell(ln=0, h=6.0, align='L', w=42.0, txt=f'{datos[2]}', border=0)    
        pdf.set_xy(17.0, 80.0)
        pdf.cell(ln=0, h=5.0, align='L', w=15.0, txt='Provincia:', border=0)
        pdf.set_xy(45.0, 80.0)
        pdf.cell(ln=0, h=5.0, align='L', w=70.0, txt=f'{datos[4]}', border=0)
        pdf.set_xy(115.0, 80.0)
        pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt='CODIGO:', border=0)
        pdf.set_xy(135.0, 80.0)
        pdf.cell(ln=0, h=5.0, align='L', w=40.0, txt=f'{datos[0]}', border=0)
        pdf.set_line_width(0.0)
        pdf.line(15.0, 88.0, 185.0, 88.0)
        pdf.set_xy(17.0, 90.0)
        pdf.cell(ln=0, h=5.0, align='L', w=48.0, txt='Numero de miembros:', border=0)
        pdf.set_xy(65.0, 90.0)
        pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt=f'{cant}', border=0)
        pdf.set_xy(92.0, 90.0)
        pdf.cell(ln=0, h=5.0, align='L', w=43.0, txt='Per\xedodo Facturado', border=0)
        pdf.set_xy(125.0, 90.0)
        pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt=f'{fecha}', border=0)
        pdf.set_xy(150.0, 90.0)
        pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt='31/01/2009', border=0)
        pdf.set_line_width(0.0)
        pdf.line(15.0, 95.0, 185.0, 95.0)
        pdf.set_font('arial', '', 11.0)
        pdf.set_xy(15.0,95.0)
        pdf.cell(w=30.0, h=10.0, txt='ID',border=1,ln=0,align='C',fill=0)
        pdf.cell(w=80.0, h=10.0, txt='NOMBRE DEL ASOCIADO',border=1,ln=0,align='C',fill=0)
        pdf.cell(w=30.0, h=10.0,txt= 'CEDULA',border=1,ln=0,align='C',fill=0)
        pdf.multi_cell(w=30.0, h=10.0, txt='APORTE',border=1,align='C',fill=0)        
        for valor in string :
                pdf.set_x(15)
                pdf.cell(w=30.0,h= 10.0, txt=(valor[0]),border=1,ln=0,align='C',fill=0)
                pdf.cell(w=80.0, h=10.0,txt=(valor[2]),border=1,ln=0,align='L',fill=0)
                pdf.cell(w=30.0, h=10.0,txt=(valor[3]),border=1,ln=0,align='C',fill=0)
                pdf.multi_cell(w=30.0, h=10.0,txt=(valor[1]),border=1,align='C',fill=0)            
        pdf.ln(5)    
        pdf.set_font('arial', 'B', 12.0)
        pdf.set_x(120)
        pdf.cell(w=0.0, h=10.0,txt=f'TOTAL APORTADO {cuotas[0]}RD$  ',border=0,ln=1,align='L',fill=0)
        pdf.set_x(120)       
        pdf.cell(w=0.0, h=10.0,txt=f'TOTAL PENDIENTES {cuotas[1]}RD$ ',border=0,ln=1,align='L',fill=0) 

        pdf.output(f"C:/Users/juanc/Desktop/proyecto motoben-actec/actec-bootrap/static/pdf/factura_{parada}{titulo}{fecha}.pdf", 'F')    
        return  str(f"/static/pdf/factura_{parada}{titulo}{fecha}.pdf") 
    
def info_cuotas(string,cuota): 
     estados=[] 
     for valor in string:
         estados += valor 
     x=estados.count('pago')
     y=estados.count('no-pago')
     pagadas=x*float(cuota)
     no_pagadas=y*float(cuota)
     return pagadas,no_pagadas