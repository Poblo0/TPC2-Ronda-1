import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.io.*;
import org.json.simple.*;
import org.json.simple.parser.*;

public class Bot {
    private char[] commands;
    private Object state;
    private char[][] map;
    private int mapWidth;
    private int mapHeight;
    private JSONArray info;
    private int bombX;
    private int bombY;

    public Bot() {
        this.commands = new char[4];
        Arrays.fill(this.commands, '_');
        this.state = null;
        this.map = null;
        this.info = null;
    }

    public void setJSON(JSONArray info) {
        this.info = info;
    }

    public void goLeft() {
        this.commands[0] = 'L';
    }

    public void goRight() {
        this.commands[1] = 'R';
    }

    public void jump() {
        this.commands[2] = 'J';
    }

    public void useBomb() {
        this.commands[3] = 'B';
    }

    public void clearCommands() {
        Arrays.fill(this.commands, '_');
    }

    public String getControls() {
        return new String(this.commands);
    }

    public void setState(Object state) {
        this.state = state;
    }

    public int getMyX() {
        return ((Long) info.get(0)).intValue();
    }

    public int getMyY() {
        return ((Long) info.get(1)).intValue();
    }

    public int getEnemyX() {
        return ((Long) info.get(4)).intValue();
    }

    public int getEnemyY() {
        return ((Long) info.get(5)).intValue();
    }

    public boolean haveBomb() {
        return ((Long) info.get(2)).intValue() == -128;
    }

    public boolean enemyHasBomb() {
        return ((Long) info.get(6)).intValue() == -128;
    }

    public Integer getMyBombX() {
        int myBomb = ((Long) info.get(2)).intValue();
        return (myBomb == -128 || myBomb == -256) ? null : myBomb;
    }

    public Integer getMyBombY() {
        int myBomb = ((Long) info.get(2)).intValue();
        return (myBomb == -128 || myBomb == -256) ? null : ((Long) info.get(3)).intValue();
    }

    public Integer getEnemyBombX() {
        int enemyBomb = ((Long) info.get(6)).intValue();
        return (enemyBomb == -128 || enemyBomb == -256) ? null : enemyBomb;
    }

    public Integer getEnemyBombY() {
        int enemyBomb = ((Long) info.get(6)).intValue();
        return (enemyBomb == -128 || enemyBomb == -256) ? null : ((Long) info.get(7)).intValue();
    }

    public void readMap(String filePath) {
        List<char[]> tempMap = new ArrayList<>();

        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                tempMap.add(line.toCharArray());
            }
        } catch (IOException e) {
            e.printStackTrace();
            return;
        }
        makeRectangle(tempMap);
    }

    private void makeRectangle(List<char[]> tempMap) {
        int maxWidth = 0;

        // Calculate max width
        for (char[] row : tempMap) {
            if (row.length > maxWidth) {
                maxWidth = row.length;
            }
        }

        // Convert List<char[]> to char[][] with padding
        int height = tempMap.size();
        map = new char[height + 2][maxWidth + 1]; // Extra rows and columns for padding

        for (int i = 0; i < height + 2; i++) {
            Arrays.fill(map[i], '_'); // Fill with '_'
        }

        for (int i = 0; i < height; i++) {
            char[] row = tempMap.get(i);
            System.arraycopy(row, 0, map[i + 1], 1, row.length); // Copy with padding
        }

        mapWidth = maxWidth + 1;
        mapHeight = height + 2;
    }

    public boolean isSolid(int x, int y) {
        if (x < 0 || x >= mapWidth || y < 0 || y >= mapHeight) {
            return false;
        }
        return this.map[y][x] == '.';
    }

    public String clientAnswer() {
        return new String(commands);
    }

    public Integer getPickUpX() {
        if (haveBomb() || enemyHasBomb())
            return null;
        else return bombX;
    }

    public Integer getPickUpY() {
        if (haveBomb() || enemyHasBomb())
            return null;
        else return bombY;
    }

    public void getInitialPos(char[][] matrix, char character) {
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[i].length; j++) {
                if (matrix[i][j] == character) {
                    bombX = j * 64 + 64;
                    bombY = i * 64 + 128;
                    return;
                }
            }
        }
    }

}
