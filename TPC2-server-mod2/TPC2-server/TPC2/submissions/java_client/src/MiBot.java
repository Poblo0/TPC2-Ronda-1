public class MiBot extends Bot {

    private int ejemploVariable;

    public MiBot() {
        super(); // Si borras esta línea, no pasa nada. Esto no es python. (Es Java que es peor)
        ejemploVariable = 0;
    }

    public void behavior() {
        // Este método se ejecutará tras cada actualización del juego
        // Introduce tu comportamiento aquí y mucha suerte
        goRight(); // Yendo a la derecha como Mario
    }
}
