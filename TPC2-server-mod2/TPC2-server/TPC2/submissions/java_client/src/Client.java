import java.io.*;
import java.net.Socket;
import org.json.simple.JSONObject;
import org.json.simple.JSONArray;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

public class Client {
    private static final String HOST = "127.0.0.1";
    private static final int PORT = 5000;

    public static void main(String[] args) {
        startClient();
    }

    public static void startClient() {
        try (Socket clientSocket = new Socket(HOST, PORT)) {
            BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
            
            // Crea el bot, le asigna el mapa y lo inicia
            MiBot bot = new MiBot();
            int round = 0;

            // Ciclo principal del cliente
            while (true) {
                // Recibir el estado del juego
                String gameState = in.readLine();
                if (gameState == null) {
                    break; // Si el servidor cierra la conexión, se sale del ciclo
                }
                System.out.println("Recivido");

                // Analizar el JSON recibido
                JSONParser parser = new JSONParser();
                JSONObject stateData = (JSONObject) parser.parse(gameState);

                // Obtener el estado del juego (en el servidor se guarda en la lista "state")
                JSONArray stateArray = (JSONArray) stateData.get("state");
                // Extraer los datos relevantes de la respuesta del servidor
                int nextGame = ((Long) stateArray.get(8)).intValue();
                
                // Verificar si es necesario reiniciar el mapa (según el valor de "next_game")
                if (nextGame == 1) {
                    round++;
                    bot.readMap("./maps/map_" + round + ".txt");
                }
                
                bot.setState(stateData); // Actualizar el estado del bot con el estado recibido

                // Obtener las pulsaciones de botones del bot
                bot.clearCommands();
                bot.behavior();
                String presses = bot.getControls();  // Debería devolver algo como "LRJB"

                // Enviar las pulsaciones de vuelta al servidor
                JSONObject outputData = new JSONObject();
                outputData.put("presses", presses);
                out.println(outputData.toString()); // Enviar las pulsaciones al servidor
                System.out.println("Enviado");

                // Esperar un poco antes de continuar (opcional para evitar saturar la red)
                Thread.sleep(100); // 100ms, ajustable
            }
        } catch (IOException | ParseException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
