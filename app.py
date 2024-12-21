import mysql.connector,funciones,os
from flask import Flask, render_template,flash, request,  redirect, url_for,make_response
from PIL import Image, ImageDraw, ImageFont
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
            cabecera = funciones.info_cabecera(cur,parada) 
            prestamos=funciones.lista_prestamos(cur,parada)
            miembros = funciones.lista_miembros(cur,parada)                
            diario = funciones.diario_general(cur,parada) 
            cuotas_hist = funciones.pendiente_aport(cur,parada)
            datos=funciones.aportacion(cur,parada) 
            nombre =  funciones.info_personal(cur,parada,cedula)
            prestamo = funciones.verificar_prestamo(cur,parada,cedula)
            pagos = funciones.hist_pago(cur,parada,nombre)        
            cur.close()           
            if cabecera[2] !=cedula:
               return render_template('index.html',informacion=informacion,cabecera=cabecera,fecha=fecha,miembros=miembros,diario=diario,cuotas_hist=cuotas_hist,nombre=nombre,prestamo=prestamo,pagos=pagos)   
            else: 
                return render_template("presidente.html",informacion=informacion,miembros=miembros,datos=datos,cabecera=cabecera,fecha=fecha,diario=diario,prestamos=prestamos,parada=parada,pagos=pagos,cuotas_hist=cuotas_hist)             
    else:
        msg = 'cedula no esta registrada!'        
        flash(msg)           
        return redirect(url_for('login'))    
            


@app.route("/cuotas", methods=["GET","POST"])
def cuotas():   
    if request.method == 'POST': 
        my_list=[]
        titulo=request.form['listado']  
        president=request.form['president'] 
        parada=request.form['parada'] 
        fecha=request.form['time']
        cant=request.form['numero']
        valor_cuota=request.form['valor']
        for i in range(int(cant)): 
            my_list +=(request.form.getlist('item')[i],
                    request.form.getlist('select')[i],
                    request.form.getlist('nombre')[i],
                    request.form.getlist('cedula')[i])  
        string=funciones.dividir_lista(my_list,4)
        info_string=funciones.info_cuotas(string, valor_cuota)
        cur = connection.cursor()     
        funciones.crear_pago(cur,parada,string,valor_cuota,fecha) 
        pdf=funciones.imprimir_lista(cur,parada,fecha,string,valor_cuota,titulo,president,cant,info_string )
        cur.close() 
        return render_template('imprimir.html',pdf=pdf) 

@app.route("/data_gastos",methods=["GET","POST"])
def data_gastos():
    if request.method == 'POST':
       titulo=request.form['gastos']  
       president=request.form['president'] 
       parada=request.form['parada'] 
       fecha=request.form['time']
       miembros=request.form['miembros']
       item = request.form['item'] 
       descripcion = request.form['descripcion_g'] 
       cantidad = request.form['cantidad_g']      
       cur = connection.cursor()    
       funciones.report_gastos(cur,parada,fecha,descripcion,cantidad)  
       pdf=funciones.imprimir(cur,parada,fecha,descripcion,cantidad,titulo,president,miembros,item)
       cur.close() 
       return render_template('imprimir.html',pdf=pdf)
        
@app.route("/data_ingresos",methods=["GET","POST"])
def data_ingresos(): 
    if request.method == 'POST':
       titulo=request.form['ingresos']  
       president=request.form['president'] 
       parada=request.form['parada'] 
       fecha=request.form['time']
       miembros=request.form['miembros']
       item = request.form['item'] 
       descripcion = request.form['descripcion_i'] 
       cantidad = request.form['cantidad_i'] 
       cur = connection.cursor() 
       funciones.report_ingresos(cur,parada,fecha,descripcion,cantidad)          
       pdf=funciones.imprimir(cur,parada,fecha,descripcion,cantidad,titulo,president,miembros,item )
       cur.close()
       return render_template('imprimir.html',pdf=pdf)
                    
@app.route("/data_prestamos",methods=["GET","POST"])
def data_prestamos(): 
    if request.method == 'POST':
       titulo=request.form['prestamos']  
       president=request.form['president'] 
       parada=request.form['parada'] 
       fecha=request.form['time']
       miembros=request.form['miembros']  
       item = request.form['item']           
       prestamo = request.form['descripcion_p'] 
       monto = request.form['cantidad_p']
       cur = connection.cursor() 
       funciones.report_prestamo(cur,parada,fecha,prestamo,monto)
       pdf=funciones.imprimir(cur,parada,fecha,prestamo,monto,titulo,president,miembros,item )          
       cur.close()
       return render_template('imprimir.html',pdf=pdf)

@app.route("/data_abonos",methods=["GET","POST"])
def data_abonos(): 
    if request.method == 'POST': 
       titulo=request.form['abonos']  
       president=request.form['president'] 
       parada=request.form['parada'] 
       fecha=request.form['time']
       miembros=request.form['miembros'] 
       item = request.form['item']       
       abono_a = request.form['descripcion_a'] 
       cantidad_a = request.form['cantidad_a']  
       cur = connection.cursor() 
       funciones.report_abono(cur,parada,fecha,abono_a,cantidad_a)          
       pdf=funciones.imprimir(cur,parada,fecha,abono_a,cantidad_a,titulo,president,miembros,item )  
       cur.close()
       return render_template('imprimir.html',pdf=pdf)
   
@app.route("/data_bancos",methods=["GET","POST"])
def data_bancos(): 
    if request.method == 'POST':
       titulo=request.form['bancaria']  
       president=request.form['president'] 
       parada=request.form['parada'] 
       fecha=request.form['time']
       miembros=request.form['miembros'] 
       banco = request.form['banco'] 
       cuenta = request.form['cuenta'] 
       movimiento = request.form['operacion']
       item = request.form['item'] 
       monto = request.form['monto']
       balance = request.form['balance']
       operacion= f"operacion de {movimiento} en la cuenta # {cuenta} de el {banco}"
       cur = connection.cursor() 
       funciones.estado_bancario(cur,parada,fecha,banco,cuenta,operacion,monto,balance)       
       pdf=funciones.imprimir(cur,parada,fecha,operacion,monto,titulo,president,miembros,item )   
       cur.close()  
       return render_template('imprimir.html',pdf=pdf)
    
@app.route("/enviar",methods=["GET","POST"])   
def enviar():
    if request.method == 'POST':
        parada=request.form['envio'] 
        print(parada)
        return
       

@app.route("/canal")
def canal():
    return render_template('canal_motoben.html')

@app.route("/presidente")
def presidente():
    return render_template('presidente.html')   

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=6800)
