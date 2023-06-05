import React, { SVGProps } from 'react';
interface PolarGridProps {
    cx?: number;
    cy?: number;
    innerRadius?: number;
    outerRadius?: number;
    polarAngles?: number[];
    polarRadius?: number[];
    gridType?: 'polygon' | 'circle';
    radialLines: boolean;
}
export declare type Props = SVGProps<SVGPathElement> & PolarGridProps;
export declare const PolarGrid: {
    (props: Props): React.JSX.Element;
    displayName: string;
    defaultProps: {
        cx: number;
        cy: number;
        innerRadius: number;
        outerRadius: number;
        gridType: string;
        radialLines: boolean;
    };
};
export {};
