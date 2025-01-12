from utils.edges import TableEdges
from utils.forces import FieldForces
import numpy as np

class KalmanFilter:
    def __init__(self, dt=1, process_noise_std=1, measurement_noise_std=1):

        self.dt = dt  # Passo temporale
        self.table_edges = TableEdges((1920, 1080))  # Riferimento ai bordi del tavolo
        self.field_forces = FieldForces((1920, 1080))  # Riferimento alle forze del campo

        # Stato: [x, y, vx, vy], inizialmente tutto a zero
        self.state = np.zeros((4, 1))  # 4x1: posizione (x, y) e velocità (vx, vy)

        # Matrice di covarianza iniziale (incertezza sullo stato)
        self.P = np.eye(4) * 1000  # Inizialmente incertezza alta
        
        # Matrice di transizione dello stato (modello di movimento)
        self.F = np.array([
            [1, 0, dt,  0],  # x = x + vx*dt
            [0, 1,  0, dt],  # y = y + vy*dt
            [0, 0,  1,  0],  # vx resta invariata
            [0, 0,  0,  1]   # vy resta invariata
        ])
        
        # Matrice di rumore del processo
        q = process_noise_std**2
        self.Q = q * np.array([
            [dt**4/4, 0, dt**3/2, 0],
            [0, dt**4/4, 0, dt**3/2],
            [dt**3/2, 0, dt**2, 0],
            [0, dt**3/2, 0, dt**2]
        ])
        
        # Matrice di osservazione (mappatura dello stato alle misurazioni)
        self.H = np.array([
            [1, 0, 0, 0],  # Misura x
            [0, 1, 0, 0]   # Misura y
        ])
        
        # Matrice di rumore della misurazione
        r = measurement_noise_std**2
        self.R = np.eye(2) * r  # Rumore solo su x e y

    def predict(self):
        """
        Predice lo stato successivo usando il modello del movimento.
        """
        # Predizione dello stato: x' = F * x
        self.state = self.F @ self.state
        
        # Predizione della covarianza: P' = F * P * F^T + Q
        self.P = self.F @ self.P @ self.F.T + self.Q

        # Gestione dei rimbalzi se la posizione è vicina a un bordo
        if self.table_edges:
            x, y = self.state[0, 0], self.state[1, 0]
            normal = self.table_edges.get_bounce_normal(x, y)
            
            if normal is not None:
                # Rimbalzo: riflessione della velocità rispetto alla normale
                vx, vy = self.state[2, 0], self.state[3, 0]
                velocity = np.array([vx, vy])
                normal = np.array(normal)

                # Riflettere la velocità: v_riflessa = v - 2 * (v · n) * n
                reflected_velocity = velocity - 2 * np.dot(velocity, normal) * normal

                # Aggiorna la velocità nello stato
                self.state[2, 0], self.state[3, 0] = reflected_velocity[0], reflected_velocity[1]

        # Applicare forze esterne dalle pendenze
        if self.field_forces:
            x, y = self.state[0, 0], self.state[1, 0]
            force_x, force_y = self.field_forces.get_force(x, y)
            # Aggiornare le velocità con l'accelerazione indotta dalle forze
            self.state[2, 0] += force_x * self.dt
            self.state[3, 0] += force_y * self.dt



    def update(self, measurement):
        """
        Aggiorna lo stato basandosi su una nuova misurazione.
        
        Args:
            measurement: Misurazione [x, y].
        """
        if measurement is None:
            return  # Se non c'è alcuna misura, non aggiornare
        # Misurazione come vettore colonna
        z = np.array(measurement).reshape(2, 1)

        # Innovazione (differenza tra misurazione e stato previsto)
        y = z - self.H @ self.state

        # Matrice di innovazione: S = H * P * H^T + R
        S = self.H @ self.P @ self.H.T + self.R

        # Guadagno di Kalman: K = P * H^T * inv(S)
        K = self.P @ self.H.T @ np.linalg.inv(S)

        # Aggiornamento dello stato: x = x + K * y
        self.state = self.state + K @ y

        # Aggiornamento della covarianza: P = (I - K * H) * P
        I = np.eye(4)
        self.P = (I - K @ self.H) @ self.P

    def get_state(self):
        """
        Ritorna lo stato attuale come array 1D.
        
        Returns:
            Array contenente [x, y, vx, vy].
        """
        return self.state.flatten()
