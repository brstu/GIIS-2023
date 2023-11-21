package com.example.spaceinvaders;

import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.application.Application;
import javafx.scene.Cursor;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.image.Image;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.TextAlignment;
import javafx.stage.Stage;
import javafx.util.Duration;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.stream.IntStream;

public class SpaceInvaders extends Application {

    private static final Random RAND = new Random();
    private static final int WIDTH = 800;
    private static final int HEIGHT = 600;
    private static final int PLAYER_SIZE = 60;

    static final Image PLAYER_IMG = new Image("D:\\Java\\SpaceInvaders\\src\\main\\resources\\images\\player.png");
    static final Image EXPLOSION_IMG = new Image("D:\\Java\\SpaceInvaders\\src\\main\\resources\\images\\explosion.png");


    static final int EXPLOSION_W = 100;
    static final int EXPLOSION_H = 100;

    static final int EXPLOSION_COLUMNS = 8;
    static final int EXPLOSION_ROWS = 8;
    static final int EXPLOSION_STEPS = 75;


    static Image ENEMY_IMG[] = {
            new Image("D:\\Java\\SpaceInvaders\\src\\main\\resources\\images\\enemy1.png"),
            new Image("D:\\Java\\SpaceInvaders\\src\\main\\resources\\images\\enemy2.png"),
            new Image("D:\\Java\\SpaceInvaders\\src\\main\\resources\\images\\enemy3.png")
    };

    final int MAX_BOMBS = 10;
    final int  MAX_SHOT = MAX_BOMBS * 2;
    boolean gameOver = false;
    private GraphicsContext gc;

    Rocket player;
    List<Shot> shots;
    List<Universe> univ;
    List<Enemy> enemies;

    private double mouseX;
    private int score;

    @Override
    public void start(Stage stage) throws Exception {
        Canvas canvas = new Canvas(WIDTH, HEIGHT);
        gc = canvas.getGraphicsContext2D();
        Timeline timeline = new Timeline(new KeyFrame(Duration.millis(100), e -> run(gc)));
        timeline.setCycleCount(Timeline.INDEFINITE);
        timeline.play();
        canvas.setCursor(Cursor.MOVE);
        canvas.setOnMouseMoved(e -> mouseX = e.getX());
        canvas.setOnMouseClicked(e ->{
            if(shots.size() < MAX_SHOT)
                shots.add(player.shot());
            if(gameOver){
                gameOver = false;
                setup();
            }
        });
        setup();
        stage.setScene(new Scene(new StackPane(canvas)));
        stage.setTitle("Space Invaders");
        stage.show();
    }

    public void setup(){
        univ = new ArrayList<>();
        shots = new ArrayList<>();
        enemies = new ArrayList<>();
        player = new Rocket(WIDTH / 2, HEIGHT - PLAYER_SIZE, PLAYER_SIZE, PLAYER_IMG);
        score = 0;
        IntStream.range(0, MAX_BOMBS).mapToObj(i -> this.newEnemy()).forEach(enemies::add);
        System.out.println("Player initialized at (" + player.posX + ", " + player.posY + ")");
    }


    private void run(GraphicsContext gc){
        gc.setFill(Color.grayRgb(20));
        gc.fillRect(0, 0, WIDTH, HEIGHT);
        gc.setTextAlign(TextAlignment.CENTER);
        gc.setFont(Font.font(20));
        gc.setFill(Color.WHITE);
        gc.fillText("Score "+ score, 60, 20);

        if(gameOver){
            gc.setFont(Font.font(35));
            gc.setFill(Color.YELLOW);
            gc.fillText("Game Over \n Your Score is: "+score+"\n Click to play again", WIDTH / 2, HEIGHT / 2.5);
        }
        univ.forEach(Universe::draw);
        player.posX = (int) mouseX;
        player.update();
        player.draw();
        shotsAndEnemies()

        gameOver = player.destroyed;
        monitorUniv();
    }

    public void monitorUniv(){
         if(RAND.nextInt(10) > 2){
            univ.add(new Universe());
        }
        for(int i = 0; i < univ.size(); i++){
            if(univ.get(i).posY > HEIGHT)
                univ.remove(i);
        }
    }

    public void shotsAndEnemies(){
        enemies.stream().peek(Rocket::update).peek(Rocket::draw).forEach(e -> {
            if (player.colide(e) && !player.exploding) {
                player.explode();
            }
        });

        for(int i = shots.size() - 1; i >= 0; i--){
            Shot shot = shots.get(i);
            if(shot.posY < 0 || shot.toRemove){
                shots.remove(i);
                continue;
            }
            shot.update();
            shot.draw();
            for(Enemy enemy : enemies){
                if(shot.colide(enemy) && !enemy.exploding){
                    score++;
                    enemy.explode();
                    shot.toRemove = true;
                }
            }
        }

        for(int i = enemies.size() - 1; i >= 0; i--){
            if(enemies.get(i).destroyed){
                enemies.set(i, newEnemy());
            }
        }
    }

    public class Rocket{

        int posX;
        int posY;
        int size;
        boolean exploding;
        boolean destroyed;
        Image img;
        int explosiveStep = 0;

        public Rocket(int posX, int posY, int size, Image img) {
            this.posX = posX;
            this.posY = posY;
            this.size = size;
            this.img = img;
            this.exploding = false;
        }

        public Shot shot(){
            return new Shot(posX+size / 2 - Shot.size / 2, posY - Shot.size);
        }

        public void update(){
            if(exploding){
                explosiveStep++;
            }
            destroyed = explosiveStep > EXPLOSION_STEPS;
        }

        public void draw(){
            if(exploding){
                gc.drawImage(EXPLOSION_IMG, explosiveStep % EXPLOSION_COLUMNS * EXPLOSION_W,
                        (explosiveStep / EXPLOSION_ROWS) * EXPLOSION_H + 1, EXPLOSION_W, EXPLOSION_H, posX, posY, size, size);
            }
            else {
                gc.drawImage(img, posX, posY, size, size);
            }
        }

        public boolean colide(Rocket other){
            int d = distance(this.posX + size / 2, this.posY + size / 2,
                    other.posX + other.size / 2, other.posY + other.size / 2);
            return d < other.size / 2 + this.size / 2;
        }

        public void explode(){
            exploding = true;
            explosiveStep = -1;
        }

    }
    public class Enemy extends Rocket{
        int Speed = (score / 5) + 2;

        public Enemy(int posX, int posY, int size, Image img) {
            super(posX, posY, size, img);
        }

        public void update(){
            super.update();
            if(!exploding && !destroyed) posY += Speed;
            if(posY > HEIGHT) destroyed = true;
        }
    }


    public class Shot{
        public boolean toRemove;
        int posX;
        int posY;
        int speed = 10;
        static final int size = 6;

        public Shot(int posX, int posY){
            this.posX = posX;
            this.posY = posY;
        }

        public void update(){
            posY -= speed;
        }

        public void draw(){
            gc.setFill(Color.RED);
            if(score >= 50 && score <= 70 || score >= 120){
                gc.setFill(Color.YELLOWGREEN);
                speed = 50;
                gc.fillRect(posX - 5, posY - 10, size + 10, size + 30);
            }
            else{
                gc.fillRect(posX, posY, size, size);
            }
        }

        public boolean colide(Rocket rocket){
            int d = distance(this.posX + size / 2, this.posY + size / 2,
                                    rocket.posX + rocket.size / 2, rocket.posY + rocket.size / 2);
            return d < rocket.size / 2 + size / 2;
        }
    }

    public class Universe{
        int posX;
        int posY;
        private  int h;
        private  int w;
        private  int r;
        private  int g;
        private  int b;
        private double opacity;


        public Universe() {
            this.posX = RAND.nextInt(WIDTH);
            this.posY = 0;
            w = RAND.nextInt(5) + 1;
            h = RAND.nextInt(5) + 1;
            r = RAND.nextInt(100) + 150;
            g = RAND.nextInt(100) + 150;
            b = RAND.nextInt(100) + 150;
            opacity = RAND.nextFloat();
            if(opacity < 0) opacity *= -1;
            if(opacity > 0.5) opacity = 0.5;
        }

        public void draw(){
            if(opacity < 0.1) opacity += 0.01;
            gc.setFill(Color.rgb(r,g,b));
            gc.fillOval(posX, posY, w, h);
            posY += 20;
        }
    }

    Enemy newEnemy(){
        return new Enemy(50 + RAND.nextInt(WIDTH - 100), 0, PLAYER_SIZE,
                ENEMY_IMG[RAND.nextInt(ENEMY_IMG.length)]);
    }
    int distance(int x1, int y1, int x2, int y2){
        return (int) Math.sqrt(Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2));
    }

    public static void main(String[] args) {
        launch();
    }
}
