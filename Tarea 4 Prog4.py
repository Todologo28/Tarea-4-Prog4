import redis
import json

# Conexión a KeyDB (similar a Redis)
client = redis.Redis(host='localhost', port=6379, db=0)

def agregar_receta():
    try:
        nombre = input("Nombre de la receta: ")
        ingredientes = input("Ingredientes (separados por comas): ")
        pasos = input("Pasos para la receta: ")

        receta = {
            'nombre': nombre,
            'ingredientes': ingredientes,
            'pasos': pasos
        }

        # Guardar la receta como JSON en un hash de KeyDB
        client.hset('recetas', nombre, json.dumps(receta))
        print("Receta agregada con éxito.")
    except Exception as e:
        print(f"Error al agregar receta: {e}")

def actualizar_receta():
    try:
        nombre_original = input("Nombre de la receta a actualizar: ")

        # Verificar si la receta existe
        if not client.hexists('recetas', nombre_original):
            print("La receta no existe.")
            return

        nuevo_nombre = input("Nuevo nombre de la receta: ")
        nuevos_ingredientes = input("Nuevos ingredientes (separados por comas): ")
        nuevos_pasos = input("Nuevos pasos: ")

        # Crear nueva receta
        receta_actualizada = {
            'nombre': nuevo_nombre,
            'ingredientes': nuevos_ingredientes,
            'pasos': nuevos_pasos
        }

        # Si el nombre cambió, eliminar la receta original
        if nombre_original != nuevo_nombre:
            client.hdel('recetas', nombre_original)

        # Guardar la receta actualizada
        client.hset('recetas', nuevo_nombre, json.dumps(receta_actualizada))
        print("Receta actualizada con éxito.")
    except Exception as e:
        print(f"Error al actualizar receta: {e}")

def eliminar_receta():
    try:
        nombre = input("Nombre de la receta a eliminar: ")

        # Eliminar la receta del hash
        resultado = client.hdel('recetas', nombre)

        if resultado:
            print("Receta eliminada con éxito.")
        else:
            print("Receta no encontrada.")
    except Exception as e:
        print(f"Error al eliminar receta: {e}")

def ver_recetas():
    try:
        # Obtener todas las recetas
        recetas = client.hkeys('recetas')

        if recetas:
            print(f"Total de recetas: {len(recetas)}")
            for receta in recetas:
                print(receta.decode('utf-8'))
        else:
            print("No hay recetas disponibles.")
    except Exception as e:
        print(f"Error al ver las recetas: {e}")

def buscar_receta():
    try:
        nombre = input("Nombre de la receta a buscar: ")

        # Obtener la receta como JSON
        receta_json = client.hget('recetas', nombre)

        if receta_json:
            receta = json.loads(receta_json)
            print(f"Ingredientes: {receta['ingredientes']}")
            print(f"Pasos: {receta['pasos']}")
        else:
            print("Receta no encontrada.")
    except Exception as e:
        print(f"Error al buscar la receta: {e}")

def menu():
    while True:
        try:
            print("\n--- Libro de Recetas ---")
            print("1. Agregar nueva receta")
            print("2. Actualizar receta existente")
            print("3. Eliminar receta")
            print("4. Ver listado de recetas")
            print("5. Buscar ingredientes y pasos de receta")
            print("6. Salir")

            opcion = input("Selecciona una opción: ")

            if opcion == '1':
                agregar_receta()
            elif opcion == '2':
                actualizar_receta()
            elif opcion == '3':
                eliminar_receta()
            elif opcion == '4':
                ver_recetas()
            elif opcion == '5':
                buscar_receta()
            elif opcion == '6':
                break
            else:
                print("Opción no válida, por favor elige otra.")
        except Exception as e:
            print(f"Error en la ejecución del programa: {e}")

if __name__ == '__main__':
    try:
        menu()
    finally:
        # Cerrar la conexión a KeyDB
        client.close()
