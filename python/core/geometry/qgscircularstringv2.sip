class QgsCircularStringV2: public QgsCurveV2
{
%TypeHeaderCode
#include <qgscircularstringv2.h>
%End

  public:
    QgsCircularStringV2();
    ~QgsCircularStringV2();

    virtual bool operator==( const QgsCurveV2& other ) const;
    virtual bool operator!=( const QgsCurveV2& other ) const;

    virtual QString geometryType() const;
    virtual int dimension() const;
    virtual QgsCircularStringV2* clone() const;
    virtual void clear();

    virtual QgsRectangle calculateBoundingBox() const;

    virtual bool fromWkb( QgsConstWkbPtr wkb );
    virtual bool fromWkt( const QString& wkt );

    int wkbSize() const;
    unsigned char* asWkb( int& binarySize ) const;
    QString asWkt( int precision = 17 ) const;
    QDomElement asGML2( QDomDocument& doc, int precision = 17, const QString& ns = "gml" ) const;
    QDomElement asGML3( QDomDocument& doc, int precision = 17, const QString& ns = "gml" ) const;
    QString asJSON( int precision = 17 ) const;

    int numPoints() const;

    /** Returns the point at index i within the circular string.
     */
    QgsPointV2 pointN( int i ) const;

    /**
     * @copydoc QgsCurveV2::points()
     */
    void points( QList<QgsPointV2>& pts ) const;

    /** Sets the circular string's points
     */
    void setPoints( const QList<QgsPointV2>& points );

    /**
     * @copydoc QgsAbstractGeometryV2::length()
     */
    virtual double length() const;

    /**
     * @copydoc QgsCurveV2::startPoint()
     */
    virtual QgsPointV2 startPoint() const;
    /**
     * @copydoc QgsCurveV2::endPoint()
     */
    virtual QgsPointV2 endPoint() const;
    /**
     * @copydoc QgsCurveV2::curveToLine()
     */
    virtual QgsLineStringV2* curveToLine() const;

    void draw( QPainter& p ) const;

    /** Transforms the geometry using a coordinate transform
     * @param ct coordinate transform
     * @param d transformation direction
     */
    void transform( const QgsCoordinateTransform& ct, QgsCoordinateTransform::TransformDirection d = QgsCoordinateTransform::ForwardTransform );
    void transform( const QTransform& t );
    void addToPainterPath( QPainterPath& path ) const;

    /**
     * @copydoc QgsCurveV2::drawAsPolygon()
     */
    void drawAsPolygon( QPainter& p ) const;

    virtual bool insertVertex( QgsVertexId position, const QgsPointV2& vertex );
    virtual bool moveVertex( QgsVertexId position, const QgsPointV2& newPos );
    virtual bool deleteVertex( QgsVertexId position );

    double closestSegment( const QgsPointV2& pt, QgsPointV2& segmentPt,  QgsVertexId& vertexAfter, bool* leftOf, double epsilon ) const;
    /**
     * @copydoc QgsCurveV2::pointAt()
     */
    bool pointAt( int i, QgsPointV2& vertex, QgsVertexId::VertexType& type ) const;

    /**
     * @copydoc QgsCurveV2::sumUpArea()
     */
    void sumUpArea( double& sum ) const;

    /**
     * @copydoc QgsAbstractGeometryV2::hasCurvedSegments()
     */
    bool hasCurvedSegments() const;

    /** Returns approximate rotation angle for a vertex. Usually average angle between adjacent segments.
        @param vertex the vertex id
        @return rotation in radians, clockwise from north*/
    double vertexAngle( QgsVertexId vertex ) const;

    virtual QgsCircularStringV2* reversed() const /Factory/;

    virtual bool addZValue( double zValue = 0 );
    virtual bool addMValue( double mValue = 0 );

    virtual bool dropZValue();
    virtual bool dropMValue();

  private:
    void segmentize( const QgsPointV2& p1, const QgsPointV2& p2, const QgsPointV2& p3, QList<QgsPointV2>& points ) const;
};
