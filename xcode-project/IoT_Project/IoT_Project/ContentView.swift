import SwiftUI
import Firebase
import FirebaseDatabase
import Combine

class RealtimeDatabaseViewModel: ObservableObject {
    @Published var entries: [Entry] = []
    @Published var entryCount: Int = 0 {
        didSet {
            updateEntries()
        }
    }

    init() {
        fetchEntryCount()
    }

    func fetchEntryCount() {
        let ref = Database.database().reference(withPath: "plantAttributes")
        ref.observeSingleEvent(of: .value) { snapshot in
            if let value = snapshot.value as? [String: String] {
                self.entries = value.map { (key, value) in
                    Entry(key: key, stringValue: value)
                }
                self.entryCount = self.entries.count
            } else {
                self.entryCount = 0
            }
        }
    }

    private func updateEntries() {
        if entries.count < entryCount {
            for _ in entries.count..<entryCount {
                entries.append(Entry(key: "New Key", stringValue: "New Value"))
            }
        } else if entries.count > entryCount {
            entries = Array(entries.prefix(entryCount))
        }
    }

    func removeEntry(at offsets: IndexSet) {
        entries.remove(atOffsets: offsets)
        entryCount = entries.count
    }

    func bindingForEntryValue(_ entry: Entry) -> Binding<String> {
        guard let index = entries.firstIndex(where: { $0.id == entry.id }) else {
            fatalError("Entry not found")
        }
        return Binding(
            get: { "\(self.entries[index].alias),\(self.entries[index].min),\(self.entries[index].max)" },
            set: { newValue in
                let components = newValue.split(separator: ",")
                guard components.count == 3 else {
                    return // Handle invalid input
                }
                self.entries[index].alias = String(components[0])
                self.entries[index].min = String(components[1])
                self.entries[index].max = String(components[2])
            }
        )
    }
    
    func updateFirebaseEntries() {
        // Fetch up-to-date sensor attribute values
        let ref0 = Database.database().reference(withPath: "plantAttributes/")
        var updates0: [String: Any] = [:]
        for entry in entries {
            updates0[entry.key] = "\(entry.alias),\(entry.min),\(entry.max)"
        }
        ref0.updateChildValues(updates0) { error, _ in
            if let error = error {
                print("Error updating Firebase: \(error)")
            } else {
                print("Firebase update successful")
            }
        }
        
        // Fetch logs of sensor attribute changes made by user
        let ref1 = Database.database().reference(withPath: "plantAttributesUpdates/")
        var updates1: [String: Any] = [:]
        var i = 0.0
        for entry in entries {
            let timestamp = Date().timeIntervalSince1970

            updates1["\(String(format: "%.0f", timestamp + i))"] = "\(entry.key);\(entry.alias),\(entry.min),\(entry.max)"
            i += 1
        }
        print("\(updates1)")
        ref1.updateChildValues(updates1) { error, _ in
            if let error = error {
                print("Error updating Firebase: \(error)")
            } else {
                print("Firebase update successful")
            }
        }
    }
}

struct Entry: Identifiable {
    var id = UUID()
    var key: String
    var alias: String
    var min: String
    var max: String
    
    init(key: String, stringValue: String) {
        self.key = key
        let components = stringValue.split(separator: ",")
        guard components.count == 3 else {
            fatalError("Invalid string format: \(stringValue)")
        }
        self.alias = String(components[0])
        self.min = String(components[1])
        self.max = String(components[2])
    }
}

struct ContentView: View {
    @StateObject private var viewModel = RealtimeDatabaseViewModel()

    var body: some View {
        NavigationView {
            VStack {
                List {
                    Text("Format:\t\talias,minMoisture,maxMoisture\nExample:\tMonstera,40,80")
                        .foregroundStyle(.gray)
                        .font(.subheadline)
                        .frame(maxWidth: .infinity, alignment: .leading)
                    ForEach(viewModel.entries) { entry in
                        // "ignoreMe" records are a workaround fix for an issue encountered with Firebase library's ability to detect records
                        if (entry.key != "ignoreMe") {
                            HStack {
                                Text(entry.key)
                                    .frame(maxWidth: .infinity, alignment: .leading)
                                TextField("Value", text: viewModel.bindingForEntryValue(entry))
                                    .textFieldStyle(RoundedBorderTextFieldStyle())
                                    .frame(maxWidth: .infinity)
                            }
                        }
                    }
                    .onDelete(perform: viewModel.removeEntry)
                }
                .navigationBarTitle("Plant Attributes")
                
                Button(action: {
                    viewModel.updateFirebaseEntries()
                }) {
                    Text("Update Database")
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.green)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                        .padding()
                }
            }
            .onAppear {
                viewModel.fetchEntryCount()
            }
        }
    }
}
