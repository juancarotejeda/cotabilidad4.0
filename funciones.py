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
    
    
def hist_pago(cur,parada,nombre,cedula): 
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

def estado_bancario(cur,parada,fecha,banco,cuenta,operacion,monto) : 
    cur.execute(f"CREATE TABLE IF NOT EXISTS {parada}_banco( id int NOT NULL AUTO_INCREMENT ,fecha VARCHAR(50)  NULL, banco VARCHAR(50) NULL, operacion VARCHAR(50) NULL,  numero_cuenta VARCHAR(50) NULL, monto DECIMAl(10,2) unsigned DEFAULT 0, balance DECIMAl(10,2) unsigned DEFAULT 0,PRIMARY KEY(id))")                                                                                                                                
    cur.execute(f"INSERT INTO {parada}_banco(fecha, banco, numero_cuenta, operacion, monto) VALUES('{fecha}', '{banco}', '{cuenta}', '{operacion}',{monto},0.00)")
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