<?xml version="1.0" encoding="UTF-8"?>
<!-- edited with XMLSpy v2010 rel. 2 (http://www.altova.com) (SunGard FRONT ARENA) -->
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:element name="ValueType" type="xs:string"/>
    <xs:element name="Value" type="xs:double"/>
    <xs:element name="Unit" type="xs:string"/>
    <xs:element name="Type" type="xs:string"/>
    <xs:element name="Time" type="xs:string"/>
    <xs:element name="TextColor" type="xs:integer"/>
    <xs:element name="TemplateId" type="xs:string"/>
    <xs:element name="Table">
        <xs:complexType>
            <xs:sequence>
                <xs:element ref="Name"/>
                <xs:element ref="Type"/>
                <xs:element ref="NumberOfColumns"/>
                <xs:element ref="Columns"/>
                <xs:element ref="Settings"/>
                <xs:element ref="Rows"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
    <xs:element name="String" type="xs:string"/>
    <xs:element name="Settings">
        <xs:complexType>
            <xs:sequence>
                <xs:element ref="Groups"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
    <xs:element name="RowType" type="xs:string"/>
    <xs:element name="Rows">
        <xs:complexType>
            <xs:sequence>
                <xs:element ref="Row" minOccurs="0" maxOccurs="unbounded"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
    <xs:element name="RowId" type="xs:string"/>
    <xs:element name="Row">
        <xs:complexType>
            <xs:sequence>
                <xs:element ref="Label"/>
                <xs:element ref="RowId"/>
                <xs:element ref="Cells"/>
                <xs:sequence maxOccurs="unbounded">
                    <xs:element ref="Rows"/>
                </xs:sequence>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
    <xs:element name="ReportContents">
        <xs:complexType>
            <xs:sequence>
                <xs:element ref="Table"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
    <xs:element name="RawData" type="xs:anyType"/>
    <xs:element name="PRIMEReport">
        <xs:complexType>
            <xs:sequence>
                <xs:element ref="Name"/>
                <xs:element ref="Type"/>
                <xs:element ref="Time"/>
                <xs:element ref="LocalTime"/>
                <xs:element ref="ArenaDataServer"/>
                <xs:element ref="ReportContents"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
    <xs:element name="NumberOfColumns" type="xs:integer"/>
    <xs:element name="Number" type="xs:double"/>
    <xs:element name="Name" type="xs:string"/>
    <xs:element name="MultiReport">
        <xs:complexType>
            <xs:sequence>
                <xs:element ref="PRIMEReport" maxOccurs="unbounded"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
    <xs:element name="LocalTime" type="xs:string"/>
    <xs:element name="Label" type="xs:string"/>
    <xs:element name="Groups">
        <xs:complexType>
            <xs:sequence>
                <xs:element ref="Group" minOccurs="0" maxOccurs="unbounded"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
    <xs:element name="GroupLabel" type="xs:string"/>
    <xs:element name="Group">
        <xs:complexType>
            <xs:sequence>
                <xs:element ref="Label"/>
                <xs:sequence maxOccurs="unbounded">
                    <xs:element ref="Column"/>
                    <xs:element ref="Cell"/>
                </xs:sequence>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
    <xs:element name="FullData">
        <xs:complexType>
            <xs:choice>
                <xs:element ref="Date"/>
                <xs:element ref="DateTime"/>
                <xs:element ref="DenominatedValue"/>
                <xs:element ref="Number"/>
                <xs:element ref="String"/>
            </xs:choice>
        </xs:complexType>
    </xs:element>
    <xs:element name="FormattedData" type="xs:string"/>
    <xs:element name="DenominatedValue">
        <xs:complexType>
            <xs:sequence>
                <xs:element ref="Value"/>
                <xs:element ref="Unit" minOccurs="0"/>
                <xs:element ref="DateTime" minOccurs="0"/>
                <xs:element ref="Type" minOccurs="0"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
    <xs:element name="DefaultData" type="xs:anyType"/>
    <xs:element name="DateTime" type="xs:string"/>
    <xs:element name="Date" type="xs:string"/>
    <xs:element name="Context" type="xs:string"/>
    <xs:element name="Columns">
        <xs:complexType>
            <xs:sequence>
                <xs:element ref="Column" minOccurs="0" maxOccurs="unbounded"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
    <xs:element name="ColumnUniqueId" type="xs:string"/>
    <xs:element name="ColumnId" type="xs:string"/>
    <xs:element name="Column">
        <xs:complexType>
            <xs:sequence>
                <xs:element ref="ColumnId" minOccurs="0"/>
                <xs:element ref="ColumnUniqueId" minOccurs="0"/>
                <xs:element ref="Context" minOccurs="0"/>
                <xs:element ref="Label" minOccurs="0"/>
                <xs:element ref="GroupLabel" minOccurs="0"/>
                <xs:element ref="TemplateId" minOccurs="0"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
    <xs:element name="Cells">
        <xs:complexType>
            <xs:sequence>
                <xs:element ref="Cell" minOccurs="0" maxOccurs="unbounded"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
    <xs:element name="Cell">
        <xs:complexType>
            <xs:choice>
                <xs:element ref="FormattedData"/>
                <xs:sequence>
                    <xs:element ref="ValueType"/>
                    <xs:choice>
                        <xs:sequence>
                            <xs:element ref="RawData"/>
                            <xs:choice minOccurs="0">
                                <xs:element ref="FormattedData"/>
                                <xs:sequence>
                                    <xs:element ref="ValueType" minOccurs="0"/>
                                    <xs:element ref="DefaultData"/>
                                    <xs:element ref="FormattedData" minOccurs="0"/>
                                </xs:sequence>
                                <xs:sequence>
                                    <xs:element ref="FullData"/>
                                    <xs:choice minOccurs="0">
                                        <xs:element ref="FormattedData"/>
                                        <xs:sequence>
                                            <xs:element ref="ValueType" minOccurs="0"/>
                                            <xs:element ref="DefaultData"/>
                                            <xs:element ref="FormattedData" minOccurs="0"/>
                                        </xs:sequence>
                                    </xs:choice>
                                </xs:sequence>
                            </xs:choice>
                        </xs:sequence>
                        <xs:sequence>
                            <xs:element ref="DefaultData"/>
                            <xs:element ref="FormattedData" minOccurs="0"/>
                        </xs:sequence>
                    </xs:choice>
                </xs:sequence>
                <xs:sequence>
                    <xs:element ref="RawData"/>
                    <xs:choice minOccurs="0">
                        <xs:element ref="FormattedData"/>
                        <xs:sequence>
                            <xs:element ref="ValueType" minOccurs="0"/>
                            <xs:element ref="DefaultData"/>
                            <xs:element ref="FormattedData" minOccurs="0"/>
                        </xs:sequence>
                        <xs:sequence>
                            <xs:element ref="FullData"/>
                            <xs:choice minOccurs="0">
                                <xs:element ref="FormattedData"/>
                                <xs:sequence>
                                    <xs:element ref="ValueType" minOccurs="0"/>
                                    <xs:element ref="DefaultData"/>
                                    <xs:element ref="FormattedData" minOccurs="0"/>
                                </xs:sequence>
                            </xs:choice>
                        </xs:sequence>
                    </xs:choice>
                </xs:sequence>
                <xs:sequence>
                    <xs:element ref="FullData"/>
                    <xs:choice minOccurs="0">
                        <xs:element ref="FormattedData"/>
                        <xs:sequence>
                            <xs:element ref="ValueType" minOccurs="0"/>
                            <xs:element ref="DefaultData"/>
                            <xs:element ref="FormattedData" minOccurs="0"/>
                        </xs:sequence>
                    </xs:choice>
                </xs:sequence>
                <xs:sequence>
                    <xs:element ref="DefaultData"/>
                    <xs:element ref="FormattedData" minOccurs="0"/>
                </xs:sequence>
                <xs:sequence>
                    <xs:element ref="Appearance"/>
                    <xs:choice>
                        <xs:element ref="FormattedData"/>
                        <xs:sequence>
                            <xs:element ref="ValueType"/>
                            <xs:choice>
                                <xs:sequence>
                                    <xs:element ref="RawData"/>
                                    <xs:choice minOccurs="0">
                                        <xs:element ref="FormattedData"/>
                                        <xs:sequence>
                                            <xs:element ref="ValueType" minOccurs="0"/>
                                            <xs:element ref="DefaultData"/>
                                            <xs:element ref="FormattedData" minOccurs="0"/>
                                        </xs:sequence>
                                        <xs:sequence>
                                            <xs:element ref="FullData"/>
                                            <xs:choice minOccurs="0">
                                                <xs:element ref="FormattedData"/>
                                                <xs:sequence>
                                                    <xs:element ref="ValueType" minOccurs="0"/>
                                                    <xs:element ref="DefaultData"/>
                                                    <xs:element ref="FormattedData" minOccurs="0"/>
                                                </xs:sequence>
                                            </xs:choice>
                                        </xs:sequence>
                                    </xs:choice>
                                </xs:sequence>
                                <xs:sequence>
                                    <xs:element ref="DefaultData"/>
                                    <xs:element ref="FormattedData" minOccurs="0"/>
                                </xs:sequence>
                            </xs:choice>
                        </xs:sequence>
                        <xs:sequence>
                            <xs:element ref="RawData"/>
                            <xs:choice minOccurs="0">
                                <xs:element ref="FormattedData"/>
                                <xs:sequence>
                                    <xs:element ref="ValueType" minOccurs="0"/>
                                    <xs:element ref="DefaultData"/>
                                    <xs:element ref="FormattedData" minOccurs="0"/>
                                </xs:sequence>
                                <xs:sequence>
                                    <xs:element ref="FullData"/>
                                    <xs:choice minOccurs="0">
                                        <xs:element ref="FormattedData"/>
                                        <xs:sequence>
                                            <xs:element ref="ValueType" minOccurs="0"/>
                                            <xs:element ref="DefaultData"/>
                                            <xs:element ref="FormattedData" minOccurs="0"/>
                                        </xs:sequence>
                                    </xs:choice>
                                </xs:sequence>
                            </xs:choice>
                        </xs:sequence>
                        <xs:sequence>
                            <xs:element ref="FullData"/>
                            <xs:choice minOccurs="0">
                                <xs:element ref="FormattedData"/>
                                <xs:sequence>
                                    <xs:element ref="ValueType" minOccurs="0"/>
                                    <xs:element ref="DefaultData"/>
                                    <xs:element ref="FormattedData" minOccurs="0"/>
                                </xs:sequence>
                            </xs:choice>
                        </xs:sequence>
                        <xs:sequence>
                            <xs:element ref="DefaultData"/>
                            <xs:element ref="FormattedData" minOccurs="0"/>
                        </xs:sequence>
                    </xs:choice>
                </xs:sequence>
            </xs:choice>
        </xs:complexType>
    </xs:element>
    <xs:element name="BkgColor" type="xs:integer"/>
    <xs:element name="ArenaDataServer" type="xs:string"/>
    <xs:element name="Appearance">
        <xs:complexType>
            <xs:sequence>
                <xs:element ref="BkgColor" minOccurs="0"/>
                <xs:element ref="TextColor" minOccurs="0"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
</xs:schema>
