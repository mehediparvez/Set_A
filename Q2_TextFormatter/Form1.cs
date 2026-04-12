using System.Drawing;
using System.Windows.Forms;

namespace Q2_TextFormatter;

public class Form1 : Form
{
    private readonly TextBox txtName = new(), txtMessage = new(), txtResult = new();
    private RadioButton rbBold, rbItalic, rbUnderline, rbRed, rbBlue, rbGreen;

    public Form1()
    {
        Text = "Text Formatter";
        ClientSize = new Size(400, 360);
        StartPosition = FormStartPosition.CenterScreen;

        Add(new Label { Text = "Name:",    Location = new Point(20, 20), AutoSize = true });
        Add(new Label { Text = "Message:", Location = new Point(20, 55), AutoSize = true });
        Add(new Label { Text = "Result:",  Location = new Point(20, 90), AutoSize = true });

        txtName.SetBounds(120, 17, 250, 20);
        txtMessage.SetBounds(120, 52, 250, 20);
        txtResult.SetBounds(20, 110, 350, 50);
        txtResult.Multiline = true;
        txtResult.Font = new Font("Segoe UI", 10F);
        Controls.AddRange(new Control[] { txtName, txtMessage, txtResult });

        var grpFmt = new GroupBox { Text = "Format", Location = new Point(20, 175), Size = new Size(350, 55) };
        AddRadio(grpFmt, "Regular", 10, true, null);
        rbBold      = AddRadio(grpFmt, "Bold",      80,  false, FontStyle.Bold);
        rbItalic    = AddRadio(grpFmt, "Italic",    160, false, FontStyle.Italic);
        rbUnderline = AddRadio(grpFmt, "Underline", 230, false, FontStyle.Underline);
        Add(grpFmt);

        var grpCol = new GroupBox { Text = "Color", Location = new Point(20, 240), Size = new Size(350, 55) };
        AddRadio(grpCol, "Black", 10, true,  null);
        rbRed   = AddRadio(grpCol, "Red",   80,  false, null);
        rbBlue  = AddRadio(grpCol, "Blue",  160, false, null);
        rbGreen = AddRadio(grpCol, "Green", 235, false, null);
        Add(grpCol);

        var btnDisplay = new Button { Text = "Display", Location = new Point(20,  310), Size = new Size(100, 30) };
        var btnClear   = new Button { Text = "Clear",   Location = new Point(140, 310), Size = new Size(100, 30) };
        var btnExit    = new Button { Text = "Exit",    Location = new Point(260, 310), Size = new Size(100, 30) };

        btnDisplay.Click += (_, _) => { txtResult.Text = $"{txtName.Text} {txtMessage.Text}"; ApplyStyle(); };
        btnClear.Click   += (_, _) => { txtName.Clear(); txtMessage.Clear(); txtResult.Clear(); };
        btnExit.Click    += (_, _) => Application.Exit();

        Controls.AddRange(new Control[] { btnDisplay, btnClear, btnExit });
    }

    private RadioButton AddRadio(GroupBox grp, string label, int x, bool isDefault, FontStyle? _)
    {
        var rb = new RadioButton { Text = label, Location = new Point(x, 22), AutoSize = true, Checked = isDefault };
        rb.CheckedChanged += (_, _) => { if (txtResult.Text.Length > 0) ApplyStyle(); };
        grp.Controls.Add(rb);
        return rb;
    }

    private void ApplyStyle()
    {
        var style = rbBold.Checked ? FontStyle.Bold : rbItalic.Checked ? FontStyle.Italic
                  : rbUnderline.Checked ? FontStyle.Underline : FontStyle.Regular;
        txtResult.Font     = new Font("Segoe UI", 10F, style);
        txtResult.ForeColor = rbRed.Checked ? Color.Red : rbBlue.Checked ? Color.Blue
                            : rbGreen.Checked ? Color.Green : Color.Black;
    }

    private void Add(Control c) => Controls.Add(c);
}
