package com.addressbookapp;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.*;
import java.util.HashMap;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;


public class Main extends JFrame {
    private JTextField nameField;
    private JTextField addressField;
    private HashMap<String, Contact> contacts;
    private Contact currentContact;
    private String selectedFilePath;

    public Main() {
        setTitle("AddressBook");
        setSize(700, 500);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JPanel topPanel = new JPanel();
        topPanel.setLayout(new BoxLayout(topPanel, BoxLayout.Y_AXIS));

        JLabel nameLabel = new JLabel("Name");
        JLabel addressLabel = new JLabel("Address:");

        nameField = new JTextField(10);
        addressField = new JTextField(10);
        addressField.setPreferredSize(new Dimension(100, 100));
        addressField.setHorizontalAlignment(JTextField.LEFT); // Изменено на LEFT

        topPanel.add(nameLabel);
        topPanel.add(nameField);
        topPanel.add(addressLabel);
        topPanel.add(addressField);


        JPanel buttonPanel = new JPanel();
        buttonPanel.setLayout(new BoxLayout(buttonPanel, BoxLayout.Y_AXIS));

        JButton addButton = new JButton("Add");
        JButton editButton = new JButton("Edit");
        JButton removeButton = new JButton("Remove");
        JButton findButton = new JButton("Find");
        JButton loadButton = new JButton("Load");
        JButton saveButton = new JButton("Save");
        JButton cancelButton = new JButton("Cancel");
        JButton exportButton = new JButton("Export");

        buttonPanel.add(addButton);
        buttonPanel.add(Box.createRigidArea(new Dimension(0, 10))); // Вертикальный отступ
        buttonPanel.add(editButton);
        buttonPanel.add(Box.createRigidArea(new Dimension(0, 10))); // Вертикальный отступ
        buttonPanel.add(removeButton);
        buttonPanel.add(Box.createRigidArea(new Dimension(0, 10))); // Вертикальный отступ
        buttonPanel.add(findButton);
        buttonPanel.add(Box.createRigidArea(new Dimension(0, 10))); // Вертикальный отступ
        buttonPanel.add(loadButton);
        buttonPanel.add(Box.createRigidArea(new Dimension(0, 10))); // Вертикальный отступ
        buttonPanel.add(saveButton);
        buttonPanel.add(Box.createRigidArea(new Dimension(0, 10))); // Вертикальный отступ
        buttonPanel.add(cancelButton);
        buttonPanel.add(Box.createRigidArea(new Dimension(0, 10))); // Вертикальный отступ
        buttonPanel.add(exportButton);

        JPanel bottomPanel = new JPanel();
        bottomPanel.setLayout(new FlowLayout(FlowLayout.RIGHT));
        JButton prevButton = new JButton("Previous");
        JButton nextButton = new JButton("Next");
        bottomPanel.add(prevButton);
        bottomPanel.add(nextButton);

        JPanel mainPanel = new JPanel();
        mainPanel.setLayout(new BorderLayout());
        mainPanel.add(topPanel, BorderLayout.CENTER);
        mainPanel.add(buttonPanel, BorderLayout.EAST);
        mainPanel.add(bottomPanel, BorderLayout.SOUTH);

        add(mainPanel);

        contacts = new HashMap<>();
        currentContact = null;

        addButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                addContact();
            }
        });

        editButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                editContact();
            }
        });

        removeButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                removeContact();
            }
        });

        prevButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                showPreviousContact();
            }
        });

        nextButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                showNextContact();
            }
        });
        findButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String searchName = JOptionPane.showInputDialog(Main.this, "Enter the name to find:");

                if (searchName != null && !searchName.isEmpty()) {
                    Contact contact = contacts.get(searchName);
                    if (contact != null) {
                        nameField.setText(contact.getName());
                        addressField.setText(contact.getAddress());
                        currentContact = contact;
                    } else {
                        JOptionPane.showMessageDialog(Main.this, "Contact not found for the name: " + searchName);
                    }
                }
            }
        });

        loadButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                JFileChooser fileChooser = new JFileChooser();
                int choice = fileChooser.showOpenDialog(Main.this);
                if (choice == JFileChooser.APPROVE_OPTION) {
                    File selectedFile = fileChooser.getSelectedFile();
                    selectedFilePath = selectedFile.getAbsolutePath(); // Сохраняем путь к файлу
                    loadFromFile(selectedFilePath);
                }
            }
        });

        saveButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                if (selectedFilePath != null) {
                    saveToFile(selectedFilePath);
                } else {
                    JFileChooser fileChooser = new JFileChooser();
                    int choice = fileChooser.showSaveDialog(Main.this);
                    if (choice == JFileChooser.APPROVE_OPTION) {
                        File selectedFile = fileChooser.getSelectedFile();
                        String filePath = selectedFile.getAbsolutePath();
                        if (!filePath.endsWith(".json")) {
                            filePath += ".json";
                        }
                        selectedFilePath = filePath;
                        saveToFile(selectedFilePath);
                    }
                }
            }
        });

        cancelButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                //cancel();
            }
        });

        exportButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                if (currentContact != null) {
                    JFileChooser fileChooser = new JFileChooser();
                    FileNameExtensionFilter filter = new FileNameExtensionFilter("VCF Files", "vcf");
                    fileChooser.setFileFilter(filter);

                    int choice = fileChooser.showSaveDialog(Main.this);

                    if (choice == JFileChooser.APPROVE_OPTION) {
                        File selectedFile = fileChooser.getSelectedFile();
                        String fileName = selectedFile.getAbsolutePath();

                        if (!fileName.endsWith(".vcf")) {
                            fileName += ".vcf";
                        }

                        try (BufferedWriter writer = new BufferedWriter(new FileWriter(fileName))) {
                            writer.write("BEGIN:VCARD");
                            writer.newLine();
                            writer.write("VERSION:3.0");
                            writer.newLine();
                            writer.write("FN:" + currentContact.getName());
                            writer.newLine();
                            writer.write("ADR;TYPE=HOME:" + currentContact.getAddress());
                            writer.newLine();
                            writer.write("END:VCARD");
                            writer.newLine();

                            JOptionPane.showMessageDialog(Main.this, "Contact exported as VCF: " + fileName);
                        } catch (IOException ex) {
                            ex.printStackTrace();
                            JOptionPane.showMessageDialog(Main.this, "Error exporting contact as VCF");
                        }
                    }
                } else {
                    JOptionPane.showMessageDialog(Main.this, "Please select a contact to export.");
                }
            }
        });
    }

    private void addContact() {
        String name = nameField.getText();
        String address = addressField.getText();

        if (name.isEmpty() || address.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Please enter a name and address.");
            return;
        }

        if (!contacts.containsKey(name)) {
            Contact newContact = new Contact(name, address);
            contacts.put(name, newContact);
            currentContact = newContact;
            JOptionPane.showMessageDialog(this, "\"" + name + "\" has been added to your address book.");
        } else {
            JOptionPane.showMessageDialog(this, "Sorry, \"" + name + "\" is already in your address book.");
        }

        clearFields();
    }

    private void saveToFile(String fileName) {
        try (FileWriter fileWriter = new FileWriter(fileName)) {
            // Создаем экземпляр Gson
            Gson gson = new GsonBuilder().setPrettyPrinting().create();

            // Преобразуем объект contacts в JSON и сохраняем в файл
            gson.toJson(contacts, fileWriter);

            JOptionPane.showMessageDialog(this, "Address book saved to " + fileName);
        } catch (IOException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(this, "Error saving address book to " + fileName);
        }
    }

    private void loadFromFile(String fileName) {
        try (FileReader fileReader = new FileReader(fileName)) {
            Gson gson = new Gson();
            contacts = gson.fromJson(fileReader, new TypeToken<HashMap<String, Contact>>() {}.getType());

            if (!contacts.isEmpty()) {
                // Вывести первый контакт в поля nameField и addressField
                Contact firstContact = contacts.values().iterator().next();
                nameField.setText(firstContact.getName());
                addressField.setText(firstContact.getAddress());
                currentContact = firstContact;
            } else {
                // Очистить поля, так как нет загруженных контактов
                clearFields();
            }

            JOptionPane.showMessageDialog(this, "Address book loaded from " + fileName);
        } catch (IOException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(this, "Error loading address book from " + fileName);
        }
    }

    private void editContact() {
        if (currentContact != null) {
            String name = nameField.getText();
            String address = addressField.getText();

            if (name.isEmpty() || address.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Please enter a name and address.");
                return;
            }

            Contact updatedContact = new Contact(name, address);
            contacts.put(name, updatedContact);
            currentContact = updatedContact;
            JOptionPane.showMessageDialog(this, "\"" + name + "\" has been updated in your address book.");
        }
    }

    private void removeContact() {
        if (currentContact != null) {
            String name = currentContact.getName();
            contacts.remove(name);
            clearFields();
            JOptionPane.showMessageDialog(this, "\"" + name + "\" has been removed from your address book.");
            showNextContact();
        }
    }

    private void clearFields() {
        nameField.setText("");
        addressField.setText("");
    }

    private void showNextContact() {
        if (currentContact != null && contacts.size() > 1) {
            String currentName = currentContact.getName();
            boolean found = false;

            for (String name : contacts.keySet()) {
                if (found) {
                    Contact nextContact = contacts.get(name);
                    nameField.setText(nextContact.getName());
                    addressField.setText(nextContact.getAddress());
                    currentContact = nextContact;
                    break;
                }
                if (name.equals(currentName)) {
                    found = true;
                }
            }
        }
    }

    private void showPreviousContact() {
        if (currentContact != null && contacts.size() > 1) {
            String currentName = currentContact.getName();
            String prevName = null;

            for (String name : contacts.keySet()) {
                if (name.equals(currentName)) {
                    break;
                }
                prevName = name;
            }

            if (prevName != null) {
                Contact prevContact = contacts.get(prevName);
                nameField.setText(prevContact.getName());
                addressField.setText(prevContact.getAddress());
                currentContact = prevContact;
            }
        }
    }

    class Contact implements Serializable {
        private String name;
        private String address;

        public Contact(String name, String address) {
            this.name = name;
            this.address = address;
        }

        public String getName() {
            return name;
        }

        public String getAddress() {
            return address;
        }

        private void writeObject(ObjectOutputStream out) throws IOException {
            out.defaultWriteObject();
            out.writeObject(name);
            out.writeObject(address);
        }

        private void readObject(ObjectInputStream in) throws IOException, ClassNotFoundException {
            in.defaultReadObject();
            name = (String) in.readObject();
            address = (String) in.readObject();
        }
    }


    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            Main form = new Main();
            form.setVisible(true);
        });
    }
}
