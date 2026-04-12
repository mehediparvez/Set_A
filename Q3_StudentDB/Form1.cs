using System;
using System.Data;
using System.Drawing;
using System.Windows.Forms;
using Microsoft.Data.Sqlite;

namespace Q3_StudentDB;

public class Form1 : Form
{
    private readonly TextBox txtRoll = new(), txtName = new(), txtMark = new();
    private readonly DataGridView dgv = new();
    private const string ConnStr = "Data Source=Studentinfo.db";

    public Form1()
    {
        Text = "Student Information";
        ClientSize = new Size(480, 390);
        StartPosition = FormStartPosition.CenterScreen;

        Controls.Add(new Label { Text = "Roll:", Location = new Point(20, 20), AutoSize = true });
        Controls.Add(new Label { Text = "Name:", Location = new Point(20, 55), AutoSize = true });
        Controls.Add(new Label { Text = "Mark:", Location = new Point(20, 90), AutoSize = true });

        txtRoll.SetBounds(120, 17, 200, 20);
        txtName.SetBounds(120, 52, 200, 20);
        txtMark.SetBounds(120, 87, 200, 20);
        Controls.AddRange(new Control[] { txtRoll, txtName, txtMark });

        var btnInsert  = new Button { Text = "Insert",   Location = new Point(20,  125), Size = new Size(90, 30) };
        var btnClear   = new Button { Text = "Clear",    Location = new Point(125, 125), Size = new Size(90, 30) };
        var btnShowAll = new Button { Text = "Show All", Location = new Point(230, 125), Size = new Size(90, 30) };

        btnInsert.Click  += Insert;
        btnClear.Click   += (_, _) => { txtRoll.Clear(); txtName.Clear(); txtMark.Clear(); };
        btnShowAll.Click += ShowAll;
        Controls.AddRange(new Control[] { btnInsert, btnClear, btnShowAll });

        dgv.SetBounds(20, 170, 440, 200);
        dgv.ReadOnly = true; dgv.AllowUserToAddRows = false;
        dgv.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
        Controls.Add(dgv);

        InitDB();
    }

    private void InitDB()
    {
        using var conn = new SqliteConnection(ConnStr);
        conn.Open();
        new SqliteCommand("CREATE TABLE IF NOT EXISTS result (roll INTEGER, name TEXT, mark REAL)", conn)
            .ExecuteNonQuery();
    }

    private void Insert(object s, EventArgs e)
    {
        if (!int.TryParse(txtRoll.Text, out int roll) ||
            !double.TryParse(txtMark.Text, out double mark) ||
            string.IsNullOrWhiteSpace(txtName.Text))
        {
            MessageBox.Show("Fill all fields correctly.", "Validation", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }
        using var conn = new SqliteConnection(ConnStr);
        conn.Open();
        var cmd = new SqliteCommand("INSERT INTO result VALUES (@r,@n,@m)", conn);
        cmd.Parameters.AddWithValue("@r", roll);
        cmd.Parameters.AddWithValue("@n", txtName.Text.Trim());
        cmd.Parameters.AddWithValue("@m", mark);
        cmd.ExecuteNonQuery();
        MessageBox.Show("Inserted!", "Success");
        txtRoll.Clear(); txtName.Clear(); txtMark.Clear();
    }

    private void ShowAll(object s, EventArgs e)
    {
        using var conn = new SqliteConnection(ConnStr);
        conn.Open();
        using var reader = new SqliteCommand("SELECT roll AS Roll, name AS Name, mark AS Mark FROM result", conn)
                               .ExecuteReader();
        var dt = new DataTable();
        dt.Load(reader);
        dgv.DataSource = dt;
    }
}
