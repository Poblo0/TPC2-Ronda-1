import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Bot {
    private char[] commands;
    private Object state;
    private char[][] map;
    private int mapWidth;
    private int mapHeight;

    public Bot() {
        this.commands = new char[4];
        Arrays.fill(this.commands, '_');
        this.state = null;
        this.map = null;
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
        return ((int[]) this.state)[0];
    }

    public int getMyY() {
        return ((int[]) this.state)[1];
    }

    public int getEnemyX() {
        return ((int[]) this.state)[4];
    }

    public int getEnemyY() {
        return ((int[]) this.state)[5];
    }

    public boolean haveBomb() {
        return ((int[]) this.state)[2] == -128;
    }

    public boolean enemyHasBomb() {
        return ((int[]) this.state)[6] == -128;
    }

    public Integer getMyBombX() {
        int myBomb = ((int[]) this.state)[2];
        return (myBomb == -128 || myBomb == -256) ? null : myBomb;
    }

    public Integer getMyBombY() {
        int myBomb = ((int[]) this.state)[2];
        return (myBomb == -128 || myBomb == -256) ? null : ((int[]) this.state)[3];
    }

    public Integer getEnemyBombX() {
        int enemyBomb = ((int[]) this.state)[6];
        return (enemyBomb == -128 || enemyBomb == -256) ? null : enemyBomb;
    }

    public Integer getEnemyBombY() {
        int enemyBomb = ((int[]) this.state)[7];
        return (enemyBomb == -128 || enemyBomb == -256) ? null : enemyBomb;
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
}
