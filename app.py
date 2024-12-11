import mysql.connector,funciones,os
from flask import Flask, render_template,flash, request,  redirect, url_for
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key=os.getenv("APP_KEY")
DB_HOST =os.getenv('DB_HOST')
DB_USERNAME =os.getenv("DB_USERNAME")
DB_PASSWORD =os.getenv("DB_PASSWORD")
DB_NAME =os.getenv("DB_NAME")

# Connect to the database
connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USERNAME,
    password=DB_PASSWORD,
    database=DB_NAME,
    autocommit=True
)

@app.route("/")
def login():                     
    return render_template('login.html')

@app.route("/verificador", methods=["GUET","POST"])
def verificador(): 
   msg = ''   
   if request.method == 'POST':        
    cedula = request.form['cedula']  
    cur = connection.cursor() 
    parada=funciones.vef_cedula(cur,cedula)   
    if parada!= []:                                                                             
            fecha = datetime.strftime(datetime.now(),"%Y %m %d - %H")            
            informacion = funciones.info_parada(cur,parada) 
            cabecera = funciones.info_cabecera(cur,parada,cedula) 
            nombre =  funciones.info_personal(cur,parada,cedula)
            prestamo = funciones.verificar_prestamo(cur,parada,cedula)
            miembros = funciones.lista_miembros(cur,parada)                
            diario = funciones.diario_general(cur,parada) 
            cuotas_hist = funciones.pendiente_aport(cur,parada)
            datos=funciones.aportacion(cur,parada) 
            pagos = funciones.hist_pago(cur,parada,nombre,cedula)
            mostrar = funciones.visibilidad(pagos[1])
            prestamos=funciones.lista_prestamos(cur,parada)
            cur.close()            
            if cabecera[2] !='Presidente':
               return render_template('index.html',informacion=informacion,cabecera=cabecera,fecha=fecha,miembros=miembros,diario=diario,cuotas_hist=cuotas_hist,nombre=nombre,prestamo=prestamo,pagos=pagos,mostrar=mostrar)   
            else: 
                return render_template("presidente.html",informacion=informacion,miembros=miembros,datos=datos,cabecera=cabecera,fecha=fecha,diario=diario,prestamos=prestamos,parada=parada)             
    else:
        msg = 'cedula no esta registrada!'        
        flash(msg)           
        return redirect(url_for('login'))    
            
@app.route("/canal")
def canal():
    return render_template('canal_motoben.html')

@app.route("/data_cuotas", methods=["GET","POST"])
def data_cuotas():
    my_list=[]
    if request.method == 'POST': 
        parada=request.form['parada'] 
        cedula=request.form['cedula_p']  
        hoy = request.form['time']
        cant=request.form['numero']
        valor_cuota=request.form['valor']
        for i in range(int(cant)): 
            my_list +=(request.form.getlist('item')[i],
                    request.form.getlist('select')[i],
                    request.form.getlist('nombre')[i],
                    request.form.getlist('cedula')[i])  
        string=funciones.dividir_lista(my_list,4)
        cur = connection.cursor()
        fecha = datetime.strftime(datetime.now(),"%Y %m %d - %H")  
        funciones.crear_p(cur,parada,string,valor_cuota,hoy)  
        informacion=funciones.info_parada(cur,parada) 
        cabecera = funciones.info_cabecera(cur,parada,cedula) 
        miembros=funciones.lista_miembros(cur,parada)
        diario=funciones.diario_general(cur,parada)
        datos=funciones.aportacion(cur,parada) 
        cuotas_hist=funciones.pendiente_aport(cur,parada)
        cur.close()  
        return render_template('presidente.html',informacion=informacion,cabecera=cabecera,miembros=miembros,datos=datos,fecha=fecha,diario=diario,cuotas_hist=cuotas_hist,parada=parada)   
    
@app.route("/data_bancos",methods=["GET","POST"])
def data_bancos(): 
    if request.method == 'POST':
       parada=request.form['parada'] 
       fecha = request.form['time']
       banco = request.form['banco'] 
       cuenta = request.form['cuenta'] 
       operacion = request.form['operacion']
       balance = request.form['balance']
       print(parada,fecha,banco,cuenta,operacion,balance)
       cur = connection.cursor() 
       funciones.estado_bancario(cur,parada,fecha,banco,cuenta,operacion,balance)      
       informacion=funciones.info_parada(cur,parada) 
       miembros=funciones.lista_miembros(cur,parada)
       diario=funciones.diario_general(cur,parada)
       datos=funciones.aportacion(cur,parada) 
       cabecera=funciones.info_cabecera(cur,parada)
       cuotas_hist=funciones.pendiente_aport(cur,parada)
       cur.close()  
       return render_template("index.html",informacion=informacion,miembros=miembros,diario=diario,datos=datos,cabecera=cabecera,fecha=fecha,cuotas_hist=cuotas_hist)  

@app.route("/data_gastos",methods=["GET","POST"])
def data_gastos():
    if request.method == 'POST':
       parada=request.form['parada']  
       fecha=request.form['time']
       descripcion_gastos = request.form['descripcion_g'] 
       cantidad_gastos = request.form['cantidad_g']
       cur = connection.cursor() 
       funciones.report_gastos(cur,parada,fecha,descripcion_gastos,cantidad_gastos)          
       informacion=funciones.info_parada(cur,parada) 
       miembros=funciones.lista_miembros(cur,parada)
       diario=funciones.diario_general(cur,parada)
       datos=funciones.aportacion(cur,parada) 
       cabecera=funciones.info_cabecera(cur,parada)
       cuotas_hist=funciones.pendiente_aport(cur,parada)
       cur.close()  
       return render_template("index.html",informacion=informacion,miembros=miembros,diario=diario,datos=datos,cabecera=cabecera,fecha=fecha,cuotas_hist=cuotas_hist)

@app.route("/data_ingresos",methods=["GET","POST"])
def data_ingresos(): 
    if request.method == 'POST':
       parada=request.form['parada'] 
       fecha=request.form['time']
       descripcion_ingreso = request.form['descripcion_i'] 
       cantidad_ingreso = request.form['cantidad_i'] 
       cur = connection.cursor() 
       funciones.report_ingresos(cur,parada,fecha,descripcion_ingreso,cantidad_ingreso)          
       informacion=funciones.info_parada(cur,parada) 
       miembros=funciones.lista_miembros(cur,parada)
       diario=funciones.diario_general(cur,parada)
       datos=funciones.aportacion(cur,parada) 
       cabecera=funciones.info_cabecera(cur,parada)
       cuotas_hist=funciones.pendiente_aport(cur,parada)
       cur.close()  
       return render_template("index.html",informacion=informacion,miembros=miembros,diario=diario,datos=datos,cabecera=cabecera,fecha=fecha,cuotas_hist=cuotas_hist)       


              
@app.route("/data_prestamos",methods=["GET","POST"])
def data_prestamos(): 
    if request.method == 'POST':
       parada=request.form['parada']             
       fecha=request.form['time']              
       prestamo = request.form['descripcion_p'] 
       monto = request.form['cantidad_p']
       cur = connection.cursor() 
       funciones.report_prestamo(cur,parada,fecha,prestamo,monto)          
       informacion=funciones.info_parada(cur,parada) 
       miembros=funciones.lista_miembros(cur,parada)
       diario=funciones.diario_general(cur,parada)
       datos=funciones.aportacion(cur,parada) 
       cabecera=funciones.info_cabecera(cur,parada)
       cuotas_hist=funciones.pendiente_aport(cur,parada)
       cur.close()  
       return render_template("index.html",informacion=informacion,miembros=miembros,diario=diario,datos=datos,cabecera=cabecera,fecha=fecha,cuotas_hist=cuotas_hist)

@app.route("/data_abonos",methods=["GET","POST"])
def data_abonos(): 
    if request.method == 'POST': 
       parada=request.form['parada']                
       fecha=request.form['time']       
       abono_a = request.form['descripcion_a'] 
       cantidad_a = request.form['cantidad_a']  
       cur = connection.cursor() 
       funciones.report_abono(cur,parada,fecha,abono_a,cantidad_a)          
       informacion=funciones.info_parada(cur,parada) 
       miembros=funciones.lista_miembros(cur,parada)
       diario=funciones.diario_general(cur,parada)
       datos=funciones.aportacion(cur,parada)
       cabecera=funciones.info_cabecera(cur,parada)
       cuotas_hist=funciones.pendiente_aport(cur,parada)
       cur.close()  
       return render_template("index.html",informacion=informacion,miembros=miembros,diario=diario,datos=datos,cabecera=cabecera,fecha=fecha,cuotas_hist=cuotas_hist)






if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=6800)
