import cv2
import numpy as np

class FieldForces:
    def __init__(self, table_size):
        self.table_width, self.table_height = table_size
        self.triangle_areas = [
            # Triangolo in alto a sinistra
            {"points": [(0, 0), (500, 0), (0, 500)], "force": (1, 1)},
            # Triangolo in alto a destra
            {"points": [(self.table_width, 0), (self.table_width - 500, 0), (self.table_width, 500)], "force": (-1, 1)},
            # Triangolo in basso a sinistra
            {"points": [(0, self.table_height), (0, self.table_height - 550), (550, self.table_height)], "force": (1, -1)},
            # Triangolo in basso a destra
            {"points": [
                (self.table_width, self.table_height),
                (self.table_width - 550, self.table_height),
                (self.table_width, self.table_height - 550)
            ], "force": (-1, -1)}
        ]

    def get_force(self, x, y):
        # Se x e y sono array NumPy, estrai i loro valori scalari
        if isinstance(x, np.ndarray):
            x = x.item()  # Estrae il valore scalare da un array NumPy
        if isinstance(y, np.ndarray):
            y = y.item()  # Estrae il valore scalare da un array NumPy

        # Verifica che x e y siano scalari
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise ValueError(f"Le coordinate x={x} e y={y} devono essere numeri scalari.")

        for area in self.triangle_areas:
            polygon = np.array(area["points"])

            # Verifica che il punto (x, y) sia una tupla di due numeri scalari
            if isinstance(x, (int, float)) and isinstance(y, (int, float)):
                if cv2.pointPolygonTest(polygon, (x, y), False) >= 0:
                    return area["force"]  # Restituisce la forza per l'area

        return (0, 0)  # Nessuna forza applicata



    def visualize_field(self, frame):

        overlay = frame.copy()

        for area in self.triangle_areas:
            # Disegna i contorni del triangolo (opzionale)
            cv2.polylines(overlay, [np.array(area["points"])], isClosed=True, color=(0, 255, 255), thickness=1)

            # Calcola la forza da applicare e aggiungi frecce
            ax, ay = area["force"]
            resolution = 40  # Distanza tra le frecce

            # Crea una maschera per disegnare solo all'interno dell'area
            triangle_mask = np.zeros((self.table_height, self.table_width), dtype=np.uint8)
            cv2.fillPoly(triangle_mask, [np.array(area["points"])], 255)

            for y in range(0, self.table_height, resolution):
                for x in range(0, self.table_width, resolution):
                    if triangle_mask[y, x] > 0:  # Disegna solo se il punto è nel triangolo
                        start_point = (x, y)
                        end_point = (int(x + ax * 20), int(y + ay * 20))  # Scala la forza per visualizzarla
                        cv2.arrowedLine(overlay, start_point, end_point, (0, 255, 0), 1, tipLength=0.4)

        # Sovrapposizione con trasparenza
        alpha = 1
        return cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
