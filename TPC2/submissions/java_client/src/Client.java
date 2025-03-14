import java.io.*;
import java.net.*;
import org.json.simple.*;
import org.json.simple.parser.*;

public class Client {
    public static void main(String[] args) {
        String servidor = "127.0.0.1"; // Asegúrate de que coincida con el del servidor
        int puerto = 5000;
        int round = 0;
        MiBot bot;

        try (Socket socket = new Socket(servidor, puerto);
             InputStreamReader entrada = new InputStreamReader(socket.getInputStream());
             BufferedReader lector = new BufferedReader(entrada);
             PrintWriter salida = new PrintWriter(socket.getOutputStream(), true)) {
            bot = new MiBot();
            bot.readMap("../../maps/map_" + round + ".txt");
            while (true) {
                // Leer el JSON completo (sin usar readLine)
                StringBuilder mensaje = new StringBuilder();
                int c;
                while ((c = lector.read()) != -1) {
                    mensaje.append((char) c);
                    if (mensaje.toString().endsWith("}")) break; // Detecta el fin del JSON
                }

                String mensajeRecibido = mensaje.toString();

                // Parsear el JSON
                JSONParser parser = new JSONParser();
                JSONObject jsonRecibido = (JSONObject) parser.parse(mensajeRecibido);

                // Obtener la lista de enteros
                JSONArray numeros = ((JSONArray) jsonRecibido.get("state"));

                if (((Long) numeros.get(8)).intValue() == 1) {
                    bot = new MiBot();
                    ++round;
                    bot.readMap("../../maps/map_" + round + ".txt");
                }

                bot.clearCommands();
                bot.setJSON((JSONArray) jsonRecibido.get("state"));
                bot.behavior();

                // Crear respuesta con 4 caracteres según los botones
                JSONObject respuestaJson = new JSONObject();
                respuestaJson.put("presses", bot.clientAnswer()); // Respuesta de ejemplo

                // Enviar la respuesta
                salida.println(respuestaJson.toJSONString());
            }

        } catch (IOException | ParseException e) {
            e.printStackTrace();
        }
    }
}
