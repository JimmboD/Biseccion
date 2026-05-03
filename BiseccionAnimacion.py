from manim import *
import math

class Biseccion(MovingCameraScene):
    def construct(self):

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Sección de modificaciones recomendadas para el usuario 
        a, b = 0.5, 4  
        n, tol, i = 15, 0.0001, 0 
        c = (a + b) / 2
        
        def f(x):
            #r, s = 1.25, 0.1
            #return (x**3) - 3*r*(x**2) + 4*(r**3)*s
            return x**3 - 6*x**2 + 11*x - 6
            
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Configuracion de la escena

        # Constantes para las gráficas
        inicial=a
        final=b

        # Recta
        def g(x, a_val, b_val):
            m = (f(b_val) - f(a_val)) / (b_val - a_val)
            return m * (x - a_val) + f(a_val)
        
        # Valores máximos y mínimos en y
        x = np.linspace(a, b, 1000)
        vmax, vmin = np.max(f(x)), np.min(f(x))
        
        # Configuración del plano
        plano = NumberPlane(
            x_range=[a-10, b+10, 1], y_range=[vmin-10, vmax+10, 1],
            x_length= b-a+20, y_length= vmax-vmin+20,
            background_line_style={"stroke_opacity": 0.4}
        ).add_coordinates()
        
        # Configuración de la cámara
        def calcular_frame(a_act, b_act):
            
            # Cálculo del centro y dimensiones del frame
            c_x = (a_act + b_act) / 2
            c_y = (vmax + vmin) / 2
            
            dist_x = abs(b_act - a_act)
            dist_y = abs(vmax - vmin)
            
            ancho = max(dist_x, dist_y * (16/9)) * 1.2
            
            posicion_camara = plano.c2p(c_x, c_y)
            return posicion_camara, ancho
        

        # Encuadre inicial
        pos_ini, ancho_ini = calcular_frame(a, b)
        self.camera.frame.move_to(pos_ini).set_width(ancho_ini)

        # Puntos
        graph = plano.plot(f, x_range=[inicial-5, final+5], color=RED, stroke_opacity=0.3)
        punto_a = Dot(point=plano.c2p(a, f(a)), color=YELLOW)
        punto_b = Dot(point=plano.c2p(b, f(b)), color=YELLOW)
        punto_c = Dot(point=plano.c2p(c, f(c)), color=WHITE)

        # Labels
        c_label = MathTex("Error: -").to_corner(UP+RIGHT).shift(LEFT*0.5)
        i_label= MathTex(f"Iteracion: 0").next_to(c_label, DOWN)
        c_point_label = MathTex("c,f(c)").next_to(punto_c, UP)

        # Factores de escala y posición
        height_factor = self.camera.frame.get_height() * 0.03
        width_factor = self.camera.frame.get_width() * 0.03

        # Actualización de los labels
        c_label.add_updater(lambda m: m.move_to(
            self.camera.frame.get_corner(UP + LEFT) + RIGHT *3*width_factor + DOWN * height_factor * 2
        ).set_height(height_factor))

        i_label.add_updater(lambda m: m.move_to(
            self.camera.frame.get_corner(UP + LEFT) + RIGHT *3*width_factor + DOWN * height_factor * 3.5
        ).set_height(height_factor))

        c_point_label.set_height(height_factor * 1.5)
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Animacion inicial
        self.play(Create(plano), Create(graph), run_time=2)
        self.play(FadeIn(punto_a), FadeIn(punto_b))

        self.wait(1)

        self.play(Write(c_label), Write(c_point_label), Write(i_label))
        
        graph_g = plano.plot(lambda x, na=a, nb=b: g(x, na, nb), x_range=[inicial-5, final+5], color=YELLOW)
        self.play(Create(graph_g))

        self.wait(0.5)

        # Bisección
        error = abs((c - a) / c)*100

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Algoritmo de bisección
        while (error > tol) and i < n:
            c = (a + b) / 2
            if (f(a) * f(c) < 0):
                nuevo_b, nuevo_a = c, a
                obj_viejo, obj_nuevo = punto_b, Dot(point=plano.c2p(nuevo_b, f(nuevo_b)), color=YELLOW)
                punto_b, b = obj_nuevo, nuevo_b

                error=abs((c - a) / c)*100
            else:
                nuevo_a, nuevo_b = c, b
                obj_viejo, obj_nuevo = punto_a, Dot(point=plano.c2p(nuevo_a, f(nuevo_a)), color=YELLOW)
                punto_a, a = obj_nuevo, nuevo_a

                error=abs((c - b) / c)*100

            nuevo_graph_g = plano.plot(lambda x, na=a, nb=b: g(x, na, nb), x_range=[inicial-5, final+5], color=YELLOW)
            punto_c = Dot(point=plano.c2p(c, f(c)), color=WHITE)
            
            # Actualizar labels
            nuevo_c_label = MathTex(f"Error: {error:.2f}\%")
            nuevo_i_label = MathTex(f"Iteracion: {i+1}").next_to(nuevo_c_label, DOWN)
            nuevo_c_point_label = MathTex(f"({c:.4f}, {f(c):.4f})").next_to(punto_c, UP)

            # Posicionar y escalar los nuevos labels
            nuevo_c_label.add_updater(lambda m: m.move_to(
                self.camera.frame.get_corner(UP + LEFT) + RIGHT *3*width_factor + DOWN * height_factor * 2
            ).set_height(height_factor))

            nuevo_i_label.add_updater(lambda m: m.move_to(
                self.camera.frame.get_corner(UP + LEFT) + RIGHT *3*width_factor + DOWN * height_factor * 3.5
            ).set_height(height_factor))

            nuevo_c_point_label.set_height(height_factor * 1.5)

            # Actualizar objetos
            self.play(
                ReplacementTransform(obj_viejo, obj_nuevo),
                ReplacementTransform(graph_g, nuevo_graph_g),
                ReplacementTransform(c_label, nuevo_c_label),
                ReplacementTransform(i_label, nuevo_i_label),
                ReplacementTransform(c_point_label, nuevo_c_point_label),
                FadeIn(punto_c),
                run_time=1
            )
            
            # Reiniciar variables
            graph_g = nuevo_graph_g
            c_label = nuevo_c_label
            i_label = nuevo_i_label
            c_point_label = nuevo_c_point_label
            self.play(FadeOut(punto_c), run_time=0.1)
            i += 1

        self.wait(0.1)