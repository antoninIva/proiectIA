# INTELIGENTA ARTIFICIALA
## Algoritmul Minimax cu Retezare Alfa-Beta
### Aplicatie: Jocul TAK

**Studenti:**
* Iva Antonin
* Barila Matei
* Costache Darius

**Indrumator:**
* Artene Codrut-Georgian

---

## 1. Descrierea problemei considerate

Proiectul de fata isi propune implementarea unui agent inteligent capabil sa joace Tak, un joc de strategie abstracta pentru doi jucatori, utilizand tehnici fundamentale de Inteligenta Artificiala. Obiectivul principal este dezvoltarea unui calculator care sa ia decizii optime impotriva unui jucator uman.

### Regulile jocului Tak
Tak se joaca pe o tabla patrata (in cazul nostru, dimensiunea aleasa este 4x4).

**Scopul jocului:** Un jucator castiga daca reuseste sa alinieze 4 piese proprii (din varful stivelor) pe o linie, o coloana sau pe una dintre diagonalele principale.

**Piesele:** Exista doua tipuri de piese implementate:
* **Piese Plate:** Pot face parte dintr-un drum si pot fi stivuite.
* **Piese Verticale:** Nu conteaza pentru drum, dar blocheaza drumurile si nu se poate pune nicio piesa peste ele (actioneaza ca ziduri).

**Mecanica jocului:** La fiecare tura, un jucator poate alege intre doua actiuni:
1. Sa plaseze o piesa noua (plata sau verticala) pe un loc liber al tablei.
2. Sa mute o piesa sau o stiva de piese deja existente pe tabla, respectand regulile de stivuire.

Complexitatea jocului provine din natura sa tridimensionala si din faptul ca tabla se modifica dinamic, nu doar prin ocuparea pozitiilor, ci si prin eliberarea lor sau blocarea strategica. Aceasta complexitate face ca Tak sa fie un candidat excelent pentru testarea algoritmului Minimax.

---

## 2. Aspecte teoretice privind algoritmul

Pentru determinarea mutarii optime a calculatorului, am utilizat algoritmul Minimax cu retezare Alfa-Beta.

### 2.1. Algoritmul Minimax
Minimax este un algoritm recursiv utilizat in teoria jocurilor si teoria deciziei pentru a minimiza pierderea maxima posibila (sau pentru a maximiza castigul minim). Algoritmul genereaza un arbore de stari ale jocului:
* **Nivelul MAX (Calculatorul):** Incearca sa maximizeze valoarea functiei de evaluare.
* **Nivelul MIN (Omul):** Se presupune ca joaca optim, incercand sa minimizeze valoarea functiei de evaluare (sa castige el sau sa reduca avantajul calculatorului).

### 2.2. Retezarea Alfa-Beta (Alpha-Beta Pruning)
Deoarece arborelui de joc pentru Tak creste exponential odata cu adancimea, explorarea completa este imposibila. Retezarea Alfa-Beta este o tehnica de optimizare care elimina ramurile din arborele de cautare care nu pot influenta decizia finala.
* **Alpha:** Cea mai buna valoare (maxima) gasita pana acum pentru jucatorul MAX.
* **Beta:** Cea mai buna valoare (minima) gasita pana acum pentru jucatorul MIN.

Daca intr-un nod MIN gasim o mutare cu valoare mai mica decat Alpha, nu mai are rost sa exploram, deoarece MAX nu va alege niciodata ramura care duce la acest nod. Similar se aplica pentru nodurile MAX si valoarea Beta.

### 2.3. Functia de Evaluare (Heuristica)
Deoarece explorarea completa a arborelui este imposibila, folosim o functie euristica avansata pentru a estima sansele de castig. In implementarea noastra, scorul unei stari se calculeaza insumand trei factori strategici:

1.  **Controlul Centrului:** Tabla este impartita in zone de importanta. Piesele care ocupa cele 4 patrate centrale (1,1), (1,2), (2,1), (2,2) primesc un bonus de puncte (+5), deoarece controlul centrului ofera mobilitate superioara.
2.  **Lungimea Lantului:** Se calculeaza cel mai lung lant de piese adiacente pentru fiecare jucator. Un lant mai lung este recompensat exponential (Lungime * 20), incurajand AI-ul sa construiasca structuri solide.
3.  **Material:** Diferenta dintre numarul de piese plate controlate de Calculator si cele ale Omului.

**Formula simplificata:**
`Eval(stare) = (BonusCentru + BonusLant + Material)_Calculator - (BonusCentru + BonusLant + Material)_Om`

---

## 3. Modalitatea de rezolvare

Aplicatia a fost dezvoltata in limbajul Python, utilizand biblioteca PyQt6 pentru interfata grafica. Arhitectura este una orientata pe obiecte, separand logica jocului de interfata cu utilizatorul.

### Componente Principale:

**Modelul (GameClasses.py, action.py):**
* `Board`: Reprezinta starea tablei (matrice 4x4), gestioneaza listele de piese si validarea regulilor. Contine metoda de verificare a victoriei (Flood Fill / BFS).
* `Piece`: Defineste proprietatile unei piese (pozitie, tip, proprietar).
* `Minimax`: Implementeaza logica recursiva de cautare.
* `Action`: Abstractie care unifica cele doua tipuri de actiuni posibile (Plasare si Mutare).

**Interfata Grafica (UI):**
* `TakGameWindow`: Fereastra principala care integreaza tabla de joc si panourile laterale.
* `BoardWidget`: Componenta vizuala care deseneaza tabla si piesele, gestioneaza animatiile de mutare si evenimentele de mouse.
* `WorkerThread`: Pentru a nu bloca interfata grafica in timp ce algoritmul "gandeste", calculul mutarii este rulat pe un fir de executie (thread) separat (QRunnable).

### Fluxul de executie:
1. Omul efectueaza o mutare prin interfata.
2. Se verifica starea de final. Daca nu este final, se activeaza MinimaxWorker.
3. Worker-ul cloneaza tabla curenta si ruleaza Minimax la adancimea selectata.
4. Cea mai buna stare rezultata este trimisa inapoi catre UI, care actualizeaza tabla vizual.

---

## 4. Listarea partilor semnificative din codul sursa

Mai jos sunt prezentate segmentele critice de cod care implementeaza logica de inteligenta artificiala.

### 4.1. Algoritmul Minimax (GameClasses.py)
Aceasta este metoda recursiva care exploreaza starile posibile.

```python
class Minimax:
    @staticmethod
    def find_next_board(current_board, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing=True):
        finished, winner = current_board.check_finish()
        if finished or depth == 0:
            return current_board

        best_board = None

        if maximizing:
            max_eval = float('-inf')

            for piece in current_board.pieces:
                if piece.player == PlayerType.Computer:
                    for move in piece.valid_moves(current_board):
                        temp_board = current_board.make_move(move)
                        
                        result = Minimax.find_next_board(
                            temp_board, depth - 1, alpha, beta, False
                        )
                        eval_score = result.evaluation_function()

                        if eval_score > max_eval:
                            max_eval = eval_score
                            best_board = temp_board

                        alpha = max(alpha, eval_score)
                        if beta <= alpha:
                            break
            
            return best_board if best_board else current_board

        else:
            min_eval = float('inf')
            
            for piece in current_board.pieces:
                if piece.player == PlayerType.Human:
                    for move in piece.valid_moves(current_board):
                        temp_board = current_board.make_move(move)

                        result = Minimax.find_next_board(
                            temp_board, depth - 1, alpha, beta, True
                        )
                        eval_score = result.evaluation_function()

                        if eval_score < min_eval:
                            min_eval = eval_score
                            best_board = temp_board

                        beta = min(beta, eval_score)
                        if beta <= alpha:
                            break
            
            return best_board if best_board else current_board
```
4.2. Functia de Evaluare si BFS (GameClasses.py)
Calculam scorul tablei bazat pe lungimea drumurilor. Se foloseste o parcurgere in latime (BFS) pentru a vedea cat de extins este lantul format de piese.
```python
def longest_road_length(self, player):
        player_top_flats = set()
        # Colectam toate piesele jucatorului care sunt deasupra
        for x in range(self.size):
            for y in range(self.size):
                p = self.get_top_piece(x, y)
                if p is not None and p.player == player and p.type == PieceType.Flat:
                    player_top_flats.add((x, y))

        if not player_top_flats:
            return 0

        max_len = 0
        visited = set()

        # Parcurgere BFS pentru a gasi lantul maxim
        for start_node in player_top_flats:
            if start_node not in visited:
                q = [start_node]
                local_visited = {start_node}
                count = 0
                while q:
                    cx, cy = q.pop(0)
                    count += 1
                    visited.add((cx, cy))

                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = cx + dx, cy + dy
                        if (nx, ny) in player_top_flats and (nx, ny) not in local_visited:
                            local_visited.add((nx, ny))
                            q.append((nx, ny))
                
                if count > max_len:
                    max_len = count
        return max_len
```
4.3. Generarea Actiunilor (GameClasses.py)
O particularitate a Tak este ca la fiecare pas poti plasa o piesa SAU muta una.
```python

def get_all_possible_next_boards(self, player):
        next_boards = []

        # 1. Generare Plasari
        if self.has_pieces_available(player):
            for x in range(self.size):
                for y in range(self.size):
                    if self.is_position_empty(x, y):
                        # Incearca plasarea unei piese Flat
                        if self.available_pieces[player][PieceType.Flat] > 0:
                            nb = self.place_piece(x, y, player, PieceType.Flat)
                            if nb: next_boards.append(nb)
                        # Incearca plasarea unui Zid 
                        if self.available_pieces[player][PieceType.Standing] > 0:
                            nb = self.place_piece(x, y, player, PieceType.Standing)
                            if nb: next_boards.append(nb)

        # 2. Generare Mutari 
        my_pieces = [p for p in self.pieces if p.player == player]
        for p in my_pieces:
            moves = p.valid_moves(self)
            for move in moves:
                nb = self.make_move(move)
                if nb: next_boards.append(nb)

        return next_boards
```
## 5. Rezultate obtinute
In aceasta sectiune sunt prezentate capturi de ecran din timpul rularii aplicatiei, ilustrand functionalitatile principale.

5.1. Configurarea Jocului
La pornirea aplicatiei, utilizatorul este intampinat de o fereastra de dialog care permite setarea dificultatii si alegerea cine incepe jocul.

<img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/0a1d5f67-c272-4d30-a248-e09790f993a2" />

5.2. Desfasurarea Jocului
Interfata principala arata tabla de joc, inventarul de piese (stanga/dreapta) si cronometrul.

<img width="500" height="400" alt="image" src="https://github.com/user-attachments/assets/ac8a36ad-2d43-444c-add5-af7c6c81cd26" />


5.3. Vizualizarea Stivelor

<img width="500" height="400" alt="image" src="https://github.com/user-attachments/assets/d15fe983-6986-44ce-95bd-73da05f2ebb2" />

5.4. Finalul Jocului
Cand o conditie de victorie este indeplinita (drum complet sau tabla plina), aplicatia anunta castigatorul.

<img width="500" height="400" alt="image" src="https://github.com/user-attachments/assets/7a4d9e54-499f-4fb5-9262-18aeaa389a32" />


Comentarii asupra performantei:
Testele au aratat ca:

Nivel Usor (Adancime 2): Mutare instantanee. AI-ul anticipeaza doar urmatoarea mutare a adversarului.

Nivel Mediu (Adancime 3): Timp de raspuns sub 1 secunda. AI-ul incepe sa blocheze incercarile evidente de aliniere ale jucatorului.

Nivel Greu (Adancime 4): Timp de raspuns 1-3 secunde. AI-ul joaca strategic, ocupand centrul si creand capcane.

Nivel Expert (Adancime 5): Timp de raspuns 3-8 secunde. Datorita retezarii Alfa-Beta, AI-ul poate explora pana la 5 mutari in avans, fiind foarte greu de invins fara o strategie perfecta.

## 6. Concluzii
Proiectul implementeaza cu succes o versiune adaptata a jocului Tak, demonstrand eficienta algoritmilor de cautare in spatiul starilor.

**Puncte forte ale implementarii**:

Interfata Grafica Reactiva: Utilizarea thread-urilor (QThread/QRunnable) asigura ca fereastra nu sta in repaus in timp ce AI-ul gandeste.

Scalabilitate: Dificultatea ajustabila permite testarea algoritmului in diverse scenarii de complexitate.

Vizualizare: Reprezentarea grafica a stivelor si a tipurilor de piese (Standing vs Flat) este intuitiva.

Limitari si directii viitoare:

Desi algoritmul este performant, limbajul Python limiteaza viteza de executie pura. O rescriere in C++ a motorului de calcul ar permite adancimi de 7-8 mutari.

Implementarea memorarea pozitiilor deja analizate ar putea reduce si mai mult timpul de calcul in finalurile de joc.

In concluzie, proiectul demonstreaza aplicabilitatea practica a algoritmilor de cautare in spatiul starilor pentru rezolvarea jocurilor de strategie.

## 7.Bibliografie
Roth, P. (2016). Tak: A Beautiful Game. Cheapass Games. (Reguli oficiale).

Documentatie Python: https://docs.python.org/3/

Documentatie PyQt6: https://www.riverbankcomputing.com/static/Docs/PyQt6/

Cursul de Inteligenta Artificiala, Laborator 7 - Algoritmul Minimax.

## 8. Contributia membrilor echipei
* **Barila Matei**: Implementarea clasei Board si a logicii de validare a mutarilor, Implementarea algoritmului Minimax si a euristicii.

* **Iva Antonin**: Dezvoltarea Interfetei Grafice (TakGameWindow, BoardWidget), integrarea animatiilor si a sistemului de threading (Worker).

* **Costache Darius**: Optimizarea algoritmului Minimax, dezvoltarea euristicii strategice, implementarea logicii corecte pentru stive si redactarea documentatiei tehnice.
