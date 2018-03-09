// ORM class for table 'null'
// WARNING: This class is AUTO-GENERATED. Modify at your own risk.
//
// Debug information:
// Generated date: Tue Mar 06 21:24:04 UTC 2018
// For connector: org.apache.sqoop.manager.GenericJdbcManager
import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.mapred.lib.db.DBWritable;
import com.cloudera.sqoop.lib.JdbcWritableBridge;
import com.cloudera.sqoop.lib.DelimiterSet;
import com.cloudera.sqoop.lib.FieldFormatter;
import com.cloudera.sqoop.lib.RecordParser;
import com.cloudera.sqoop.lib.BooleanParser;
import com.cloudera.sqoop.lib.BlobRef;
import com.cloudera.sqoop.lib.ClobRef;
import com.cloudera.sqoop.lib.LargeObjectLoader;
import com.cloudera.sqoop.lib.SqoopRecord;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.CharBuffer;
import java.sql.Date;
import java.sql.Time;
import java.sql.Timestamp;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

public class QueryResult extends SqoopRecord  implements DBWritable, Writable {
  private final int PROTOCOL_VERSION = 3;
  public int getClassFormatVersion() { return PROTOCOL_VERSION; }
  protected ResultSet __cur_result_set;
  private Long mktsrcid;
  public Long get_mktsrcid() {
    return mktsrcid;
  }
  public void set_mktsrcid(Long mktsrcid) {
    this.mktsrcid = mktsrcid;
  }
  public QueryResult with_mktsrcid(Long mktsrcid) {
    this.mktsrcid = mktsrcid;
    return this;
  }
  private String mktsrcguid;
  public String get_mktsrcguid() {
    return mktsrcguid;
  }
  public void set_mktsrcguid(String mktsrcguid) {
    this.mktsrcguid = mktsrcguid;
  }
  public QueryResult with_mktsrcguid(String mktsrcguid) {
    this.mktsrcguid = mktsrcguid;
    return this;
  }
  private String htlguid;
  public String get_htlguid() {
    return htlguid;
  }
  public void set_htlguid(String htlguid) {
    this.htlguid = htlguid;
  }
  public QueryResult with_htlguid(String htlguid) {
    this.htlguid = htlguid;
    return this;
  }
  private String chnguid;
  public String get_chnguid() {
    return chnguid;
  }
  public void set_chnguid(String chnguid) {
    this.chnguid = chnguid;
  }
  public QueryResult with_chnguid(String chnguid) {
    this.chnguid = chnguid;
    return this;
  }
  private String mktsrccd;
  public String get_mktsrccd() {
    return mktsrccd;
  }
  public void set_mktsrccd(String mktsrccd) {
    this.mktsrccd = mktsrccd;
  }
  public QueryResult with_mktsrccd(String mktsrccd) {
    this.mktsrccd = mktsrccd;
    return this;
  }
  private String createdt;
  public String get_createdt() {
    return createdt;
  }
  public void set_createdt(String createdt) {
    this.createdt = createdt;
  }
  public QueryResult with_createdt(String createdt) {
    this.createdt = createdt;
    return this;
  }
  private String updatedt;
  public String get_updatedt() {
    return updatedt;
  }
  public void set_updatedt(String updatedt) {
    this.updatedt = updatedt;
  }
  public QueryResult with_updatedt(String updatedt) {
    this.updatedt = updatedt;
    return this;
  }
  private Long langid;
  public Long get_langid() {
    return langid;
  }
  public void set_langid(Long langid) {
    this.langid = langid;
  }
  public QueryResult with_langid(Long langid) {
    this.langid = langid;
    return this;
  }
  private String mktsrcnm;
  public String get_mktsrcnm() {
    return mktsrcnm;
  }
  public void set_mktsrcnm(String mktsrcnm) {
    this.mktsrcnm = mktsrcnm;
  }
  public QueryResult with_mktsrcnm(String mktsrcnm) {
    this.mktsrcnm = mktsrcnm;
    return this;
  }
  private String mktsrcdesc;
  public String get_mktsrcdesc() {
    return mktsrcdesc;
  }
  public void set_mktsrcdesc(String mktsrcdesc) {
    this.mktsrcdesc = mktsrcdesc;
  }
  public QueryResult with_mktsrcdesc(String mktsrcdesc) {
    this.mktsrcdesc = mktsrcdesc;
    return this;
  }
  private Long htlid;
  public Long get_htlid() {
    return htlid;
  }
  public void set_htlid(Long htlid) {
    this.htlid = htlid;
  }
  public QueryResult with_htlid(Long htlid) {
    this.htlid = htlid;
    return this;
  }
  private Long chnid;
  public Long get_chnid() {
    return chnid;
  }
  public void set_chnid(Long chnid) {
    this.chnid = chnid;
  }
  public QueryResult with_chnid(Long chnid) {
    this.chnid = chnid;
    return this;
  }
  private String tdwloaddatetime;
  public String get_tdwloaddatetime() {
    return tdwloaddatetime;
  }
  public void set_tdwloaddatetime(String tdwloaddatetime) {
    this.tdwloaddatetime = tdwloaddatetime;
  }
  public QueryResult with_tdwloaddatetime(String tdwloaddatetime) {
    this.tdwloaddatetime = tdwloaddatetime;
    return this;
  }
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (!(o instanceof QueryResult)) {
      return false;
    }
    QueryResult that = (QueryResult) o;
    boolean equal = true;
    equal = equal && (this.mktsrcid == null ? that.mktsrcid == null : this.mktsrcid.equals(that.mktsrcid));
    equal = equal && (this.mktsrcguid == null ? that.mktsrcguid == null : this.mktsrcguid.equals(that.mktsrcguid));
    equal = equal && (this.htlguid == null ? that.htlguid == null : this.htlguid.equals(that.htlguid));
    equal = equal && (this.chnguid == null ? that.chnguid == null : this.chnguid.equals(that.chnguid));
    equal = equal && (this.mktsrccd == null ? that.mktsrccd == null : this.mktsrccd.equals(that.mktsrccd));
    equal = equal && (this.createdt == null ? that.createdt == null : this.createdt.equals(that.createdt));
    equal = equal && (this.updatedt == null ? that.updatedt == null : this.updatedt.equals(that.updatedt));
    equal = equal && (this.langid == null ? that.langid == null : this.langid.equals(that.langid));
    equal = equal && (this.mktsrcnm == null ? that.mktsrcnm == null : this.mktsrcnm.equals(that.mktsrcnm));
    equal = equal && (this.mktsrcdesc == null ? that.mktsrcdesc == null : this.mktsrcdesc.equals(that.mktsrcdesc));
    equal = equal && (this.htlid == null ? that.htlid == null : this.htlid.equals(that.htlid));
    equal = equal && (this.chnid == null ? that.chnid == null : this.chnid.equals(that.chnid));
    equal = equal && (this.tdwloaddatetime == null ? that.tdwloaddatetime == null : this.tdwloaddatetime.equals(that.tdwloaddatetime));
    return equal;
  }
  public boolean equals0(Object o) {
    if (this == o) {
      return true;
    }
    if (!(o instanceof QueryResult)) {
      return false;
    }
    QueryResult that = (QueryResult) o;
    boolean equal = true;
    equal = equal && (this.mktsrcid == null ? that.mktsrcid == null : this.mktsrcid.equals(that.mktsrcid));
    equal = equal && (this.mktsrcguid == null ? that.mktsrcguid == null : this.mktsrcguid.equals(that.mktsrcguid));
    equal = equal && (this.htlguid == null ? that.htlguid == null : this.htlguid.equals(that.htlguid));
    equal = equal && (this.chnguid == null ? that.chnguid == null : this.chnguid.equals(that.chnguid));
    equal = equal && (this.mktsrccd == null ? that.mktsrccd == null : this.mktsrccd.equals(that.mktsrccd));
    equal = equal && (this.createdt == null ? that.createdt == null : this.createdt.equals(that.createdt));
    equal = equal && (this.updatedt == null ? that.updatedt == null : this.updatedt.equals(that.updatedt));
    equal = equal && (this.langid == null ? that.langid == null : this.langid.equals(that.langid));
    equal = equal && (this.mktsrcnm == null ? that.mktsrcnm == null : this.mktsrcnm.equals(that.mktsrcnm));
    equal = equal && (this.mktsrcdesc == null ? that.mktsrcdesc == null : this.mktsrcdesc.equals(that.mktsrcdesc));
    equal = equal && (this.htlid == null ? that.htlid == null : this.htlid.equals(that.htlid));
    equal = equal && (this.chnid == null ? that.chnid == null : this.chnid.equals(that.chnid));
    equal = equal && (this.tdwloaddatetime == null ? that.tdwloaddatetime == null : this.tdwloaddatetime.equals(that.tdwloaddatetime));
    return equal;
  }
  public void readFields(ResultSet __dbResults) throws SQLException {
    this.__cur_result_set = __dbResults;
    this.mktsrcid = JdbcWritableBridge.readLong(1, __dbResults);
    this.mktsrcguid = JdbcWritableBridge.readString(2, __dbResults);
    this.htlguid = JdbcWritableBridge.readString(3, __dbResults);
    this.chnguid = JdbcWritableBridge.readString(4, __dbResults);
    this.mktsrccd = JdbcWritableBridge.readString(5, __dbResults);
    this.createdt = JdbcWritableBridge.readString(6, __dbResults);
    this.updatedt = JdbcWritableBridge.readString(7, __dbResults);
    this.langid = JdbcWritableBridge.readLong(8, __dbResults);
    this.mktsrcnm = JdbcWritableBridge.readString(9, __dbResults);
    this.mktsrcdesc = JdbcWritableBridge.readString(10, __dbResults);
    this.htlid = JdbcWritableBridge.readLong(11, __dbResults);
    this.chnid = JdbcWritableBridge.readLong(12, __dbResults);
    this.tdwloaddatetime = JdbcWritableBridge.readString(13, __dbResults);
  }
  public void readFields0(ResultSet __dbResults) throws SQLException {
    this.mktsrcid = JdbcWritableBridge.readLong(1, __dbResults);
    this.mktsrcguid = JdbcWritableBridge.readString(2, __dbResults);
    this.htlguid = JdbcWritableBridge.readString(3, __dbResults);
    this.chnguid = JdbcWritableBridge.readString(4, __dbResults);
    this.mktsrccd = JdbcWritableBridge.readString(5, __dbResults);
    this.createdt = JdbcWritableBridge.readString(6, __dbResults);
    this.updatedt = JdbcWritableBridge.readString(7, __dbResults);
    this.langid = JdbcWritableBridge.readLong(8, __dbResults);
    this.mktsrcnm = JdbcWritableBridge.readString(9, __dbResults);
    this.mktsrcdesc = JdbcWritableBridge.readString(10, __dbResults);
    this.htlid = JdbcWritableBridge.readLong(11, __dbResults);
    this.chnid = JdbcWritableBridge.readLong(12, __dbResults);
    this.tdwloaddatetime = JdbcWritableBridge.readString(13, __dbResults);
  }
  public void loadLargeObjects(LargeObjectLoader __loader)
      throws SQLException, IOException, InterruptedException {
  }
  public void loadLargeObjects0(LargeObjectLoader __loader)
      throws SQLException, IOException, InterruptedException {
  }
  public void write(PreparedStatement __dbStmt) throws SQLException {
    write(__dbStmt, 0);
  }

  public int write(PreparedStatement __dbStmt, int __off) throws SQLException {
    JdbcWritableBridge.writeLong(mktsrcid, 1 + __off, -5, __dbStmt);
    JdbcWritableBridge.writeString(mktsrcguid, 2 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(htlguid, 3 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(chnguid, 4 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(mktsrccd, 5 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(createdt, 6 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(updatedt, 7 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeLong(langid, 8 + __off, -5, __dbStmt);
    JdbcWritableBridge.writeString(mktsrcnm, 9 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(mktsrcdesc, 10 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeLong(htlid, 11 + __off, -5, __dbStmt);
    JdbcWritableBridge.writeLong(chnid, 12 + __off, -5, __dbStmt);
    JdbcWritableBridge.writeString(tdwloaddatetime, 13 + __off, 12, __dbStmt);
    return 13;
  }
  public void write0(PreparedStatement __dbStmt, int __off) throws SQLException {
    JdbcWritableBridge.writeLong(mktsrcid, 1 + __off, -5, __dbStmt);
    JdbcWritableBridge.writeString(mktsrcguid, 2 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(htlguid, 3 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(chnguid, 4 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(mktsrccd, 5 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(createdt, 6 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(updatedt, 7 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeLong(langid, 8 + __off, -5, __dbStmt);
    JdbcWritableBridge.writeString(mktsrcnm, 9 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(mktsrcdesc, 10 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeLong(htlid, 11 + __off, -5, __dbStmt);
    JdbcWritableBridge.writeLong(chnid, 12 + __off, -5, __dbStmt);
    JdbcWritableBridge.writeString(tdwloaddatetime, 13 + __off, 12, __dbStmt);
  }
  public void readFields(DataInput __dataIn) throws IOException {
this.readFields0(__dataIn);  }
  public void readFields0(DataInput __dataIn) throws IOException {
    if (__dataIn.readBoolean()) { 
        this.mktsrcid = null;
    } else {
    this.mktsrcid = Long.valueOf(__dataIn.readLong());
    }
    if (__dataIn.readBoolean()) { 
        this.mktsrcguid = null;
    } else {
    this.mktsrcguid = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.htlguid = null;
    } else {
    this.htlguid = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.chnguid = null;
    } else {
    this.chnguid = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.mktsrccd = null;
    } else {
    this.mktsrccd = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.createdt = null;
    } else {
    this.createdt = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.updatedt = null;
    } else {
    this.updatedt = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.langid = null;
    } else {
    this.langid = Long.valueOf(__dataIn.readLong());
    }
    if (__dataIn.readBoolean()) { 
        this.mktsrcnm = null;
    } else {
    this.mktsrcnm = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.mktsrcdesc = null;
    } else {
    this.mktsrcdesc = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.htlid = null;
    } else {
    this.htlid = Long.valueOf(__dataIn.readLong());
    }
    if (__dataIn.readBoolean()) { 
        this.chnid = null;
    } else {
    this.chnid = Long.valueOf(__dataIn.readLong());
    }
    if (__dataIn.readBoolean()) { 
        this.tdwloaddatetime = null;
    } else {
    this.tdwloaddatetime = Text.readString(__dataIn);
    }
  }
  public void write(DataOutput __dataOut) throws IOException {
    if (null == this.mktsrcid) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.mktsrcid);
    }
    if (null == this.mktsrcguid) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, mktsrcguid);
    }
    if (null == this.htlguid) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, htlguid);
    }
    if (null == this.chnguid) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, chnguid);
    }
    if (null == this.mktsrccd) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, mktsrccd);
    }
    if (null == this.createdt) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, createdt);
    }
    if (null == this.updatedt) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, updatedt);
    }
    if (null == this.langid) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.langid);
    }
    if (null == this.mktsrcnm) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, mktsrcnm);
    }
    if (null == this.mktsrcdesc) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, mktsrcdesc);
    }
    if (null == this.htlid) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.htlid);
    }
    if (null == this.chnid) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.chnid);
    }
    if (null == this.tdwloaddatetime) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, tdwloaddatetime);
    }
  }
  public void write0(DataOutput __dataOut) throws IOException {
    if (null == this.mktsrcid) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.mktsrcid);
    }
    if (null == this.mktsrcguid) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, mktsrcguid);
    }
    if (null == this.htlguid) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, htlguid);
    }
    if (null == this.chnguid) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, chnguid);
    }
    if (null == this.mktsrccd) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, mktsrccd);
    }
    if (null == this.createdt) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, createdt);
    }
    if (null == this.updatedt) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, updatedt);
    }
    if (null == this.langid) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.langid);
    }
    if (null == this.mktsrcnm) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, mktsrcnm);
    }
    if (null == this.mktsrcdesc) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, mktsrcdesc);
    }
    if (null == this.htlid) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.htlid);
    }
    if (null == this.chnid) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.chnid);
    }
    if (null == this.tdwloaddatetime) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, tdwloaddatetime);
    }
  }
  private static final DelimiterSet __outputDelimiters = new DelimiterSet((char) 44, (char) 10, (char) 0, (char) 0, false);
  public String toString() {
    return toString(__outputDelimiters, true);
  }
  public String toString(DelimiterSet delimiters) {
    return toString(delimiters, true);
  }
  public String toString(boolean useRecordDelim) {
    return toString(__outputDelimiters, useRecordDelim);
  }
  public String toString(DelimiterSet delimiters, boolean useRecordDelim) {
    StringBuilder __sb = new StringBuilder();
    char fieldDelim = delimiters.getFieldsTerminatedBy();
    __sb.append(FieldFormatter.escapeAndEnclose(mktsrcid==null?"null":"" + mktsrcid, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(mktsrcguid==null?"null":mktsrcguid, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(htlguid==null?"null":htlguid, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(chnguid==null?"null":chnguid, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(mktsrccd==null?"null":mktsrccd, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(createdt==null?"null":createdt, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(updatedt==null?"null":updatedt, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(langid==null?"null":"" + langid, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(mktsrcnm==null?"null":mktsrcnm, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(mktsrcdesc==null?"null":mktsrcdesc, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(htlid==null?"null":"" + htlid, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(chnid==null?"null":"" + chnid, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(tdwloaddatetime==null?"null":tdwloaddatetime, delimiters));
    if (useRecordDelim) {
      __sb.append(delimiters.getLinesTerminatedBy());
    }
    return __sb.toString();
  }
  public void toString0(DelimiterSet delimiters, StringBuilder __sb, char fieldDelim) {
    __sb.append(FieldFormatter.escapeAndEnclose(mktsrcid==null?"null":"" + mktsrcid, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(mktsrcguid==null?"null":mktsrcguid, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(htlguid==null?"null":htlguid, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(chnguid==null?"null":chnguid, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(mktsrccd==null?"null":mktsrccd, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(createdt==null?"null":createdt, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(updatedt==null?"null":updatedt, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(langid==null?"null":"" + langid, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(mktsrcnm==null?"null":mktsrcnm, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(mktsrcdesc==null?"null":mktsrcdesc, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(htlid==null?"null":"" + htlid, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(chnid==null?"null":"" + chnid, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(tdwloaddatetime==null?"null":tdwloaddatetime, delimiters));
  }
  private static final DelimiterSet __inputDelimiters = new DelimiterSet((char) 44, (char) 10, (char) 0, (char) 0, false);
  private RecordParser __parser;
  public void parse(Text __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(CharSequence __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(byte [] __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(char [] __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(ByteBuffer __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(CharBuffer __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  private void __loadFromFields(List<String> fields) {
    Iterator<String> __it = fields.listIterator();
    String __cur_str = null;
    try {
    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.mktsrcid = null; } else {
      this.mktsrcid = Long.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.mktsrcguid = null; } else {
      this.mktsrcguid = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.htlguid = null; } else {
      this.htlguid = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.chnguid = null; } else {
      this.chnguid = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.mktsrccd = null; } else {
      this.mktsrccd = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.createdt = null; } else {
      this.createdt = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.updatedt = null; } else {
      this.updatedt = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.langid = null; } else {
      this.langid = Long.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.mktsrcnm = null; } else {
      this.mktsrcnm = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.mktsrcdesc = null; } else {
      this.mktsrcdesc = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.htlid = null; } else {
      this.htlid = Long.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.chnid = null; } else {
      this.chnid = Long.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.tdwloaddatetime = null; } else {
      this.tdwloaddatetime = __cur_str;
    }

    } catch (RuntimeException e) {    throw new RuntimeException("Can't parse input data: '" + __cur_str + "'", e);    }  }

  private void __loadFromFields0(Iterator<String> __it) {
    String __cur_str = null;
    try {
    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.mktsrcid = null; } else {
      this.mktsrcid = Long.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.mktsrcguid = null; } else {
      this.mktsrcguid = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.htlguid = null; } else {
      this.htlguid = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.chnguid = null; } else {
      this.chnguid = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.mktsrccd = null; } else {
      this.mktsrccd = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.createdt = null; } else {
      this.createdt = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.updatedt = null; } else {
      this.updatedt = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.langid = null; } else {
      this.langid = Long.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.mktsrcnm = null; } else {
      this.mktsrcnm = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.mktsrcdesc = null; } else {
      this.mktsrcdesc = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.htlid = null; } else {
      this.htlid = Long.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.chnid = null; } else {
      this.chnid = Long.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.tdwloaddatetime = null; } else {
      this.tdwloaddatetime = __cur_str;
    }

    } catch (RuntimeException e) {    throw new RuntimeException("Can't parse input data: '" + __cur_str + "'", e);    }  }

  public Object clone() throws CloneNotSupportedException {
    QueryResult o = (QueryResult) super.clone();
    return o;
  }

  public void clone0(QueryResult o) throws CloneNotSupportedException {
  }

  public Map<String, Object> getFieldMap() {
    Map<String, Object> __sqoop$field_map = new TreeMap<String, Object>();
    __sqoop$field_map.put("mktsrcid", this.mktsrcid);
    __sqoop$field_map.put("mktsrcguid", this.mktsrcguid);
    __sqoop$field_map.put("htlguid", this.htlguid);
    __sqoop$field_map.put("chnguid", this.chnguid);
    __sqoop$field_map.put("mktsrccd", this.mktsrccd);
    __sqoop$field_map.put("createdt", this.createdt);
    __sqoop$field_map.put("updatedt", this.updatedt);
    __sqoop$field_map.put("langid", this.langid);
    __sqoop$field_map.put("mktsrcnm", this.mktsrcnm);
    __sqoop$field_map.put("mktsrcdesc", this.mktsrcdesc);
    __sqoop$field_map.put("htlid", this.htlid);
    __sqoop$field_map.put("chnid", this.chnid);
    __sqoop$field_map.put("tdwloaddatetime", this.tdwloaddatetime);
    return __sqoop$field_map;
  }

  public void getFieldMap0(Map<String, Object> __sqoop$field_map) {
    __sqoop$field_map.put("mktsrcid", this.mktsrcid);
    __sqoop$field_map.put("mktsrcguid", this.mktsrcguid);
    __sqoop$field_map.put("htlguid", this.htlguid);
    __sqoop$field_map.put("chnguid", this.chnguid);
    __sqoop$field_map.put("mktsrccd", this.mktsrccd);
    __sqoop$field_map.put("createdt", this.createdt);
    __sqoop$field_map.put("updatedt", this.updatedt);
    __sqoop$field_map.put("langid", this.langid);
    __sqoop$field_map.put("mktsrcnm", this.mktsrcnm);
    __sqoop$field_map.put("mktsrcdesc", this.mktsrcdesc);
    __sqoop$field_map.put("htlid", this.htlid);
    __sqoop$field_map.put("chnid", this.chnid);
    __sqoop$field_map.put("tdwloaddatetime", this.tdwloaddatetime);
  }

  public void setField(String __fieldName, Object __fieldVal) {
    if ("mktsrcid".equals(__fieldName)) {
      this.mktsrcid = (Long) __fieldVal;
    }
    else    if ("mktsrcguid".equals(__fieldName)) {
      this.mktsrcguid = (String) __fieldVal;
    }
    else    if ("htlguid".equals(__fieldName)) {
      this.htlguid = (String) __fieldVal;
    }
    else    if ("chnguid".equals(__fieldName)) {
      this.chnguid = (String) __fieldVal;
    }
    else    if ("mktsrccd".equals(__fieldName)) {
      this.mktsrccd = (String) __fieldVal;
    }
    else    if ("createdt".equals(__fieldName)) {
      this.createdt = (String) __fieldVal;
    }
    else    if ("updatedt".equals(__fieldName)) {
      this.updatedt = (String) __fieldVal;
    }
    else    if ("langid".equals(__fieldName)) {
      this.langid = (Long) __fieldVal;
    }
    else    if ("mktsrcnm".equals(__fieldName)) {
      this.mktsrcnm = (String) __fieldVal;
    }
    else    if ("mktsrcdesc".equals(__fieldName)) {
      this.mktsrcdesc = (String) __fieldVal;
    }
    else    if ("htlid".equals(__fieldName)) {
      this.htlid = (Long) __fieldVal;
    }
    else    if ("chnid".equals(__fieldName)) {
      this.chnid = (Long) __fieldVal;
    }
    else    if ("tdwloaddatetime".equals(__fieldName)) {
      this.tdwloaddatetime = (String) __fieldVal;
    }
    else {
      throw new RuntimeException("No such field: " + __fieldName);
    }
  }
  public boolean setField0(String __fieldName, Object __fieldVal) {
    if ("mktsrcid".equals(__fieldName)) {
      this.mktsrcid = (Long) __fieldVal;
      return true;
    }
    else    if ("mktsrcguid".equals(__fieldName)) {
      this.mktsrcguid = (String) __fieldVal;
      return true;
    }
    else    if ("htlguid".equals(__fieldName)) {
      this.htlguid = (String) __fieldVal;
      return true;
    }
    else    if ("chnguid".equals(__fieldName)) {
      this.chnguid = (String) __fieldVal;
      return true;
    }
    else    if ("mktsrccd".equals(__fieldName)) {
      this.mktsrccd = (String) __fieldVal;
      return true;
    }
    else    if ("createdt".equals(__fieldName)) {
      this.createdt = (String) __fieldVal;
      return true;
    }
    else    if ("updatedt".equals(__fieldName)) {
      this.updatedt = (String) __fieldVal;
      return true;
    }
    else    if ("langid".equals(__fieldName)) {
      this.langid = (Long) __fieldVal;
      return true;
    }
    else    if ("mktsrcnm".equals(__fieldName)) {
      this.mktsrcnm = (String) __fieldVal;
      return true;
    }
    else    if ("mktsrcdesc".equals(__fieldName)) {
      this.mktsrcdesc = (String) __fieldVal;
      return true;
    }
    else    if ("htlid".equals(__fieldName)) {
      this.htlid = (Long) __fieldVal;
      return true;
    }
    else    if ("chnid".equals(__fieldName)) {
      this.chnid = (Long) __fieldVal;
      return true;
    }
    else    if ("tdwloaddatetime".equals(__fieldName)) {
      this.tdwloaddatetime = (String) __fieldVal;
      return true;
    }
    else {
      return false;    }
  }
}
