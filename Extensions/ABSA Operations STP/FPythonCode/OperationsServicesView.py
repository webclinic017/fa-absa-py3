"""
-------------------------------------------------------------------------------
MODULE
    OperationsServicesView


DESCRIPTION
    GUI application to easily track the established connections with the ADS by the
    Operations ATS's. This is due to recurring issues observed when not all ATS's
    connect to the same ADS in the current multi ADS setup

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-07-15     FAOPS-566        Stuart Wilson           Kgomotso Gumbo          Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import clr
from datetime import datetime
import re

import acm
import FUxCore
import FUxNet


WinForms = clr.System.Windows.Forms
Color = clr.System.Drawing.Color
ListSortDirection = clr.System.ComponentModel.ListSortDirection
DATETIME_FORMATTER = acm.FDomain['datetime'].DefaultFormatter()


class OperationsServicesDialog(FUxCore.LayoutDialog):
    """
    Dialog used to select a Fixed Amount cash flow.
    """

    def __init__(self):
        """
        Constructor.
        """
        self._server_connections = self.get_active_connections()
        self._default_server_name = self._get_environment_server_name_to_connect_to()
        self._dialog = None
        self._layout = None
        self.connection_grid = None

    @FUxCore.aux_cb
    def HandleCreate(self, dialog, layout):
        """
        AUX hook called to create the dialog.
        """
        self._dialog = dialog
        self._layout = layout
        self._dialog.Caption('Operations Services View')
        self.connection_grid = self._create_connection_grid()
        cash_flow_panel = self._layout.GetControl('ops_service_view').GetCustomControl()
        cash_flow_panel.Padding = WinForms.Padding(1)
        cash_flow_panel.BackColor = Color.Gray
        cash_flow_panel.Controls.Add(self.connection_grid)

    @FUxCore.aux_cb
    def HandleApply(self):
        """
        AUX hook called when the user presses the OK button.

        Returns a value to allow the dialog to close, None to prevent
        it.
        """

        self.connection_grid = self._delete_outdated_rows(self.connection_grid)
        self._server_connections = self.get_active_connections()
        self._create_server_connections_grid_rows(self.connection_grid)
        self._highlight_rows(self.connection_grid)
        self.connection_grid.Update()

    @FUxCore.aux_cb
    def HandleCancel(self):
        """
        AUX hook called when the user cancels or closes the dialog.

        Returns a value to allow the dialog to close, None to prevent
        it.
        """
        return True

    def GetLayoutBuilder(self):
        """
        Gets a layout builder for the dialog.
        """
        layout_builder = acm.FUxLayoutBuilder()
        layout_builder.BeginVertBox('None')
        FUxNet.AddWinFormsControlToBuilder(layout_builder, 'ops_service_view', 'System.Windows.Forms.Panel',
                                           'System.Windows.Forms', 1200, 500)
        layout_builder.BeginHorzBox('None')
        layout_builder.AddButton('ok', 'Refresh')
        layout_builder.AddButton('cancel', 'Cancel')
        layout_builder.EndBox()
        layout_builder.EndBox()
        return layout_builder

    def _create_connection_grid(self):
        """
        Create the cash flow grid control.
        """
        Server_grid = WinForms.DataGridView()
        Server_grid.ColumnHeadersHeightSizeMode = WinForms.DataGridViewColumnHeadersHeightSizeMode.DisableResizing
        Server_grid.AllowUserToAddRows = False
        Server_grid.AllowUserToDeleteRows = False
        Server_grid.AllowUserToResizeRows = False
        Server_grid.ReadOnly = True
        Server_grid.SelectionMode = WinForms.DataGridViewSelectionMode.CellSelect
        Server_grid.MultiSelect = False
        Server_grid.Dock = WinForms.DockStyle.Fill
        Server_grid.AutoSizeRowsMode = WinForms.DataGridViewAutoSizeRowsMode.DisplayedCellsExceptHeaders
        Server_grid.ColumnHeadersBorderStyle = WinForms.DataGridViewHeaderBorderStyle.Single
        Server_grid.CellBorderStyle = WinForms.DataGridViewCellBorderStyle.Single
        Server_grid.RowHeadersBorderStyle = WinForms.DataGridViewHeaderBorderStyle.Single
        Server_grid.GridColor = Color.WhiteSmoke
        Server_grid.BackgroundColor = Color.White
        Server_grid.RowHeadersVisible = False
        Server_grid.BorderStyle = WinForms.BorderStyle.None
        self._create_server_connections_grid_columns(Server_grid)
        self._create_server_connections_grid_rows(Server_grid)
        self._highlight_rows(Server_grid)
        return Server_grid

    def _create_server_connections_grid_columns(self, server_grid):
        """
        Create the cash flow grid columns.
        """
        server_grid.ColumnCount = 9
        server_grid.Columns[0].Name = 'Application'
        server_grid.Columns[0].Width = 200
        server_grid.Columns[1].Name = 'Status'
        server_grid.Columns[1].Width = 80
        server_grid.Columns[2].Name = 'Server Name'
        server_grid.Columns[2].Width = 80
        server_grid.Columns[3].Name = 'OS User'
        server_grid.Columns[3].Width = 150
        server_grid.Columns[4].Name = 'User Name'
        server_grid.Columns[4].Width = 150
        server_grid.Columns[5].Name = 'Msg In'
        server_grid.Columns[5].Width = 60
        server_grid.Columns[6].Name = 'Host'
        server_grid.Columns[6].Width = 150
        server_grid.Columns[7].Name = 'Connected Time'
        server_grid.Columns[7].Width = 150
        server_grid.Columns[8].Name = 'Update Time'
        server_grid.Columns[8].Width = 150

    def _create_server_connections_grid_rows(self, server_grid):
        """
        Create the cash flow grid rows.
        """
        for connection in self._server_connections:
            server_grid.Rows.Add([
                self._remove_version_dates(connection.ApplicationName()),
                connection.Status(),
                connection.ServerName(),
                connection.OsUser(),
                connection.UserName(),
                connection.MessagesReceived(),
                connection.Host(),
                DATETIME_FORMATTER.Format(acm.Time.DateTimeFromTime(connection.ConnectTime())),
                DATETIME_FORMATTER.Format(acm.Time.DateTimeFromTime(connection.UpdateTime()))
            ])
        server_grid.Sort(server_grid.Columns[0], ListSortDirection.Ascending)

    def _remove_version_dates(self, app_name):

        new_name = re.sub("_[0-9]{4}.[0-9].[0-9]{1}_[0-9]*.[0-9.]*", "", app_name)
        return new_name.upper()

    def _delete_outdated_rows(self, connection_grid):

        while connection_grid.Rows.Count != 0:
            connection_grid.Rows.Remove(connection_grid.Rows[0])

        return connection_grid

    def _highlight_rows(self, server_grid):
        """
        Sets the row selection of the cash flow grid.
        """
        if self._default_server_name:
            for row in server_grid.Rows:

                if str(row.Cells[2].Value) != self._default_server_name:
                    row.DefaultCellStyle.BackColor = Color.Yellow
                    row.Cells[2].Style.BackColor = Color.Red

                if str(row.Cells[7].Value)[:10] < acm.Time.DateToday():
                    row.DefaultCellStyle.BackColor = Color.Yellow
                    row.Cells[7].Style.BackColor = Color.Red

                update_time = datetime.strptime(str(row.Cells[8].Value), '%Y-%m-%d %I:%M:%S %p')
                time_now = datetime.strptime(acm.Time.TimeNow(), '%Y-%m-%d %H:%M:%S.%f')

                time_delta = time_now - update_time

                if time_delta.seconds > 1200:
                    row.DefaultCellStyle.BackColor = Color.SkyBlue
                    row.Cells[8].Style.BackColor = Color.Yellow

    def get_active_connections(self):
        connections = acm.FServerConnections.Select("status=1")
        ops_services = list()
        for conn in connections:
            update_time = DATETIME_FORMATTER.Format(acm.Time.DateTimeFromTime(conn.UpdateTime()))
            if '(bg)' in conn.ApplicationName():
                continue

            if update_time[:10] < acm.Time.DateToday():
                continue

            if 'ops' in conn.ApplicationName():
                ops_services.append(conn)
                continue

            if 'swift' in conn.ApplicationName():
                ops_services.append(conn)
                continue

            if 'conf' in conn.ApplicationName():
                ops_services.append(conn)
                continue

            if 'stlm' in conn.ApplicationName():
                ops_services.append(conn)
                continue

        return ops_services

    def _get_environment_server_name_to_connect_to(self):
        if acm.FInstallationData.Select('').At(0).Name() == 'Production':
            return 'ADS_PRODA1'

        elif acm.FInstallationData.Select('').At(0).Name() == 'Playground':
            return 'ADS_DEV1'

        elif acm.FInstallationData.Select('').At(0).Name() == 'PTS_UAT':
            return "ADS_UATA9"

        else:
            return None


def run_gui(eii):

    dialog = OperationsServicesDialog()
    shell = eii.Parameter('shell')
    acm.UX.Dialogs().ShowCustomDialog(shell, dialog.GetLayoutBuilder(), dialog)
