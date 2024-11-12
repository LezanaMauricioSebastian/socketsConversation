import java.io.*; 
import java.net.*;
import java.awt.*;
import javax.swing.*;

public class ChatClient {
    private String username;
    private String hostIP;
    private int port;
    private Socket socket;
    private BufferedReader reader;
    private PrintWriter writer;

    private JFrame frame;
    private JTextArea chatArea;
    private JTextField messageField;
    private JTextField usernameField;
    private JTextField hostField;
    private JTextField portField;
    private JButton connectButton;

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new ChatClient().createAndShowGUI());
        
    }

    private void createAndShowGUI() {
        frame = new JFrame("Chat Cliente");
        frame.setSize(500, 500);  // Aumentar el tamaño de la ventana
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JPanel topPanel = new JPanel(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5); // Espaciado entre componentes

        // Campos de usuario, host y puerto
        JLabel usernameLabel = new JLabel("Nombre de usuario:");
        gbc.gridx = 0;
        gbc.gridy = 0;
        topPanel.add(usernameLabel, gbc);

        usernameField = new JTextField(10);
        gbc.gridx = 1;
        gbc.gridy = 0;
        topPanel.add(usernameField, gbc);

        JLabel hostLabel = new JLabel("Host IP:");
        gbc.gridx = 0;
        gbc.gridy = 1;
        topPanel.add(hostLabel, gbc);

        hostField = new JTextField(10);
        gbc.gridx = 1;
        gbc.gridy = 1;
        topPanel.add(hostField, gbc);

        JLabel portLabel = new JLabel("Puerto:");
        gbc.gridx = 0;
        gbc.gridy = 2;
        topPanel.add(portLabel, gbc);

        portField = new JTextField(5);
        gbc.gridx = 1;
        gbc.gridy = 2;
        topPanel.add(portField, gbc);

        connectButton = new JButton("Conectar");
        connectButton.addActionListener(e -> connectToServer());
        gbc.gridx = 1;
        gbc.gridy = 3;
        topPanel.add(connectButton, gbc);

        frame.add(topPanel, BorderLayout.NORTH);

        chatArea = new JTextArea();
        chatArea.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(chatArea);
        frame.add(scrollPane, BorderLayout.CENTER);

        JPanel bottomPanel = new JPanel(new BorderLayout());

        messageField = new JTextField();
        messageField.addActionListener(e -> sendMessage());
        bottomPanel.add(messageField, BorderLayout.CENTER);
        messageField.setEnabled(false); 
        JButton sendButton = new JButton("Enviar");
        sendButton.addActionListener(e -> sendMessage());
        bottomPanel.add(sendButton, BorderLayout.EAST);
 
        frame.add(bottomPanel, BorderLayout.SOUTH);
        frame.setVisible(true);

        
    }


    private void connectToServer() {
        username = usernameField.getText().trim();
        hostIP = hostField.getText().trim();
        try {
            port = Integer.parseInt(portField.getText().trim());
        } catch (NumberFormatException e) {
            JOptionPane.showMessageDialog(frame, "Por favor, ingresa un puerto válido.");
            return;
        }

        if (username.isEmpty() || hostIP.isEmpty()) {
            JOptionPane.showMessageDialog(frame, "Por favor, ingresa todos los datos.");
            return;
        }

        try {
            socket = new Socket(hostIP, port);
            writer = new PrintWriter(socket.getOutputStream(), true);
            reader = new BufferedReader(new InputStreamReader(socket.getInputStream(),"UTF-8"));
            

            
            writer.println(username); // Fixed: Send username with a newline

            // Start a thread to listen for messages from the server
            new Thread(this::receiveMessages).start();

            chatArea.append("Conexión exitosa al servidor\n");

            // Disable connection fields
            connectButton.setEnabled(false);
            usernameField.setEnabled(false);
            hostField.setEnabled(false);
            portField.setEnabled(false);
            messageField.setEnabled(true); // Enable message field after connecting
            
        } catch (IOException e) {
            JOptionPane.showMessageDialog(frame, "No se pudo conectar al servidor");
        }
    }

    private void sendMessage() {
        String message = messageField.getText().trim();
        if (message.isEmpty()) return;

        if (message.equals("/quitar")) {
            writer.println(message);
            closeConnection();
            frame.dispose();
        } else if (message.equals("/listar")) {
            writer.println(message); // Send the /listar command to the server
        } else {
            String fullMessage = username + ": " + message;
            chatArea.append(fullMessage + "\n"); // Show the user's own message in the chat
            writer.println(fullMessage); // Send the message to the server
        }

        messageField.setText(""); // Clear the message field
    }
private void receiveMessages() {
    String message;
    try {
        while (true) {
            message=reader.readLine();
            String receivedMessage = message; // Declare a Ffinal or effectively final variable
          
                        
            if (receivedMessage.startsWith("@username")) {              
                SwingUtilities.invokeLater(() -> chatArea.append("EL usuario "+username+" se ha conectado al chat"));
            } else {
                SwingUtilities.invokeLater(() -> chatArea.append("\n"+ receivedMessage + "\n")); // Use the final variable
            }

        }
    } catch (IOException e) {
        SwingUtilities.invokeLater(() -> chatArea.append("Conexión perdida con el servidor.\n"));
        e.printStackTrace();
    }
}
    private void closeConnection() {
        try {
            if (socket != null) socket.close();
            if (reader != null) reader.close();
            if (writer != null) writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
